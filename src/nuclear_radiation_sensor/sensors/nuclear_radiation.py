import logging
logger = logging.getLogger("morse." + __name__)

from nuclear_radiation_sensor.tools.material import MaterialCatalogue
from morse.core.sensor import Sensor
from morse.helpers.components import add_data, add_property


class NuclearRadiation(Sensor):
    """Nuclear radiation sensor measuring (effective) dose rate. A material has
    to be assigned to all objects in the scene. Some materials emits nuclear
    radiation, e. g. if "235U" (the Uranium isotope 235) is assigned to an
    object it turns it into a radiation source.
    Radiation interacts with matter, therefore shielding properties have to be
    known. This is the reason why all other objects also need a material
    assigned.
    If the shielding properties (half-value layer) is not known it is treated as
    vacuum (no shielding).
    Assigning a material is done through a property named "Material". All
    available values can be found in the class MaterialCatalogue.

    The calculation of the radiation is based on the IAEA's publication
    "Generic procedures for assessment and response during a radiological
    emergency", available at:
    http://www-pub.iaea.org/mtcd/publications/pdf/te_1162_prn.pdf
    """
    _name = "NuclearRadiation"
    _short_desc = "Generic nuclear radiation sensor."

    # exported data fields
    add_data("dose_rate", 0.0, "float",
             "Dose rate [mGy/h]")
    add_data("effective_dose_rate", 0.0, "float",
             "Effective dose rate [mSv/h]")

    # configuration properties
    add_property("dynamic_sources", False, "dynamic_sources", "boolean",
                 "if set the sensor updates the list of nuclear radiation \
                  sources every time before calculating radiation")
    add_property("surrounding_material_name", "Air", "surrounding_material_name", "string",
                 "name of the surrounding material (usually 'Air')")

    def __init__(self, obj, parent=None):
        logger.info("%s initialization", obj.name)
        Sensor.__init__(self, obj, parent)

        self.source_list = self.get_source_list()
        self.surrounding_material = MaterialCatalogue.instance().\
            get_material_by_name(self.surrounding_material_name)
        logger.info("Component initialized")

    def default_action(self):
        """ Main loop of the sensor.

        Searches for radioactive materials in the scene and shoots a ray in that
        direction. Intersected objects influence the radiation depending on the
        material they are made of.
        """
        if self.dynamic_sources:
            self.source_list = self.get_source_list()

        dose_rate = 0
        effective_dose_rate = 0
        for source in self.source_list:
            hit_list = self.cast_ray(source)
            for radiation in MaterialCatalogue.instance().get_radiation(source, self.bge_object):
                logger.debug("Overall distance to source: %f", self.bge_object.getDistanceTo(source) * 100.0)
                logger.debug("Distance inside source object: %f", (
                    hit_list[0][2] - hit_list[0][0].worldPosition).length * 100.0)
                for i in range(len(hit_list) - 1):
                    surrounding_distance = (hit_list[i][2] - hit_list[i + 1][1]).length * 100.0
                    logger.debug("Distance inside surrounding material: %f" % surrounding_distance)
                    radiation = self.surrounding_material.get_reduced_radiation(radiation, surrounding_distance)
                    obj = hit_list[i + 1][0]
                    if obj is not self.bge_object:
                        in_object_distance = (hit_list[i + 1][1] - hit_list[i + 1][2]).length * 100.0
                        material = MaterialCatalogue.instance().get_material_of_object(obj)
                        radiation = material.get_reduced_radiation(radiation, in_object_distance)
                        logger.debug("Distance inside %s: %f", material.name, in_object_distance)
                dose_rate += radiation.dose_rate
                effective_dose_rate += radiation.effective_dose_rate
        logger.debug("Dose rate: %fmGy/h", dose_rate)
        logger.debug("Effective dose rate: %fmSv/h", effective_dose_rate)
        self.local_data["dose_rate"] = dose_rate
        self.local_data["effective_dose_rate"] = effective_dose_rate

    def get_source_list(self):
        """Updates the list of all nuclear radiation sources found in the
        Simulation scene.
        """
        source_list = list()
        for obj in self.bge_object.scene.objects:
            try:
                material = MaterialCatalogue.instance().get_material_of_object(obj)
                if material.radioactivity is not None:
                    try:
                        obj["Volume"]
                    except KeyError:
                        volume = obj.worldScale[0] * obj.worldScale[1] * \
                            obj.worldScale[2]
                        obj["Volume"] = volume * 1e6  # convert to cm^3

                    source_list.append(obj)
            except KeyError:
                pass
        logger.debug("Found %d source(s)", len(source_list))
        return source_list

    def cast_ray(self, source_object):
        """Casts a ray from source_object to self and returns a list of all
        objects in the way. Each entry is a tuple (object, entry_point,
        exit_point). The source and target themselves are also contained, but in
        case of the source the entry_point, in case of the target the exit_point
        is set to None.
        """
        hit_objects = list()
        hit = None
        source = source_object
        target = self.bge_object
        hit_objects.append((source, None, None))
        while hit != target:
            hit, entry_point, _ = self.bge_object.rayCast(target, source)
            if hit is None:  # handle NO_COLLISION sensor
                hit = target
                entry_point = target.worldPosition
            hit_objects.append((hit, entry_point, None))
            source = entry_point

        # cast a ray in opposite direction to get hit points on the other side
        for i in reversed(range(len(hit_objects) - 1)):
            source_point = hit_objects[i + 1][1]
            target_point = hit_objects[i][1] if i > 0 else hit_objects[0][0].worldPosition
            _, exit_point, _ = self.bge_object.rayCast(target_point, source_point)
            if exit_point is None:  # handle NO_COLLISION sensor
                exit_point = target_point
            hit_objects[i] = (hit_objects[i][0], hit_objects[i][1],
                              exit_point)
        return hit_objects