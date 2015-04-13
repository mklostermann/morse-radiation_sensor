"""This module allows to deal with various properties of different materials,
especially radioactivity. References:
[1] "Generic procedures for assessment and response during a radiological
    emergency" by IAEA, available at:
    http://www-pub.iaea.org/mtcd/publications/pdf/te_1162_prn.pdf
[2] "Table of Radioactive Isotopes", Edgardo Browne and Richard B. Firestone,
    ISBN 0-471-84909-X
[3] "REACTOR PHYSICS CALCULATIONS ON MOX FUEL IN BOILING WATER REACTORS (BWRs)",
    Christophe Demazière, available at:
    https://www.oecd-nea.org/pt/docs/iem/jeju02/session5/SectionV-12.pdf
[4] "Spent Fuel Reprocessing Options", by IAEA, available at:
    http://www-pub.iaea.org/MTCD/Publications/PDF/TE_1587_web.pdf
"""

from morse.core import blenderapi


class MaterialCatalogue:
    """Singleton catalogue of materials. The different material instances can be
    accessed by there name(s) using this catalogue. The material of an object can
    also be directly determined by its BGE object.
    """
    _instance = None

    def __init__(self):
        if MaterialCatalogue._instance is not None:
            raise RuntimeError("This class is a singleton and should only be \
                                created and accessed via instance()")
        # conversion factors and HVLs from "Procedure E1: Point Source"
        #   [1, p. 85 et seqq.]
        # density and half life from [2]
        # density of UOX fuel from [3]
        # mass fractions from [4, p. 74]
        self._material = {"24Na": Material("24Na", None,
                                           Radioactivity(0.969, 24,
                                                         14.659 / 8760, 5.1e-7,
                                                         3.8e-7)),
                          "234U": Material("234U", None,
                                           Radioactivity(18.92, 234, 245.5e3,
                                                         1.8E-08, 2.8E-10)),
                          "235U": Material("235U", None,
                                           Radioactivity(18.92, 235, 7.04e8,
                                                         7.4e-8, 1.4e-8)),
                          "238U": Material("238U", None,
                                           Radioactivity(18.92, 238, 4.468e9,
                                                         1.5e-8, 2.3e-10)),
                          "238Pu": Material("238Pu", None,
                                            Radioactivity(19.80, 238, 87.74,
                                                          8.8e-9, 3.0e-10)),
                          "239Pu": Material("239Pu", None,
                                            Radioactivity(19.80, 239, 2.41e4,
                                                          3.4e-9, 1.2e-10)),
                          "240Pu": Material("240Pu", None,
                                            Radioactivity(19.80, 240, 6.5e3,
                                                          8.4e-9, 2.8e-10)),
                          "242Pu": Material("242Pu", None,
                                            Radioactivity(19.80, 242, 3.73e5,
                                                          6.9e-9, 2.3e-10)),
                          "UOX-4.5": Compound("UOX-4.5", 10.3,
                                              [("235U", 0.045),
                                               ("238U", 0.955)]),
                          "Lead": Material("Lead",
                                           {"24Na": 1.32, "234U": 0.01,
                                            "235U": 0.09,
                                            "238U": 0.01, "238Pu": 0.01,
                                            "239Pu": 0.01, "240Pu": 0.01,
                                            "242Pu": 0.01}, None),
                          "Iron": Material("Iron",
                                           {"24Na": 2.14, "234U": 0.04,
                                            "235U": 0.46,
                                            "238U": 0.04, "238Pu": 0.04,
                                            "239Pu": 0.04, "240Pu": 0.04,
                                            "242Pu": 0.04}, None),
                          "Water": Material("Water",
                                            {"24Na": 14.75, "234U": 0.28,
                                             "235U": 3.19,
                                             "238U": 0.27, "238Pu": 0.27,
                                             "239Pu": 0.29, "240Pu": 0.27,
                                             "242Pu": 0.27}, None),
                          "Air": Material("Air",
                                          {"24Na": 1.27e4, "234U": 2.42E+02,
                                           "235U": 2.81e3,
                                           "238U": 2.36e2, "238Pu": 2.37E+02,
                                           "239Pu": 2.58E+02, "240Pu": 2.37E+02,
                                           "242Pu": 2.37E+02}, None),
                          "Concrete": Material("Concrete",
                                               {"24Na": 6.88, "234U": 0.13,
                                                "235U": 1.51, "238U": 0.13,
                                                "238Pu": 0.13, "239Pu": 0.14,
                                                "240Pu": 0.13, "242Pu": 0.13},
                                               None)}

    @staticmethod
    def instance():
        """Get an instance of the material catalogue. Synchronisation is not
        necessary because MORSE executes everything in a single thread.
        """
        if MaterialCatalogue._instance is None:
            MaterialCatalogue._instance = MaterialCatalogue()
        return MaterialCatalogue._instance

    def get_radiation(self, source_object, target_object):
        """Returns the radiation caused by the given BGE object point source
        received at the target object or None."""
        material = self.get_material_of_object(source_object)
        if material.radioactivity is None:
            return None
        else:
            distance = source_object.getDistanceTo(target_object)
            volume = float(source_object["Volume"])
            return material.get_radiation(volume, distance)

    def get_material_of_object(self, bge_object):
        """Returns the material of a given BGE object.
        """
        return self._material[bge_object["Material"]]

    def get_material_by_name(self, name):
        """Returns the material by its name."""
        return self._material[name]


class Material:
    """This class provides data about the properties and behaviour of some
    material.
    """
    def __init__(self, name, hvl, radioactivity):
        """Initialisation setting name, density [g/cm^3], half-value layers,
        and radioactivity.
        The HVL has to be supplied as dictionary with the source radionuclide as
        key and the corresponding HVL [cm] as value.
        """
        self.name = name
        self.hvl = hvl
        self.radioactivity = radioactivity
        self.t_created = blenderapi.persistantstorage().time.time

    def get_radiation(self, volume, distance):
        """Returns the radiation emitted by a point source with volume [cm^3] of
        this material transmitted to a point at given distance [m], ignoring any
        shielding effects. None is returned if this material is not radioactive.
        The result is a list, to allow objects consisting of several radioactive
        components.
        """
        if self.radioactivity is None:
            return None
        else:
            # formula according to "Activity Calculation" [1, p. 121]
            elapsed = blenderapi.persistantstorage().time.time - self.t_created
            specific_activity = self.radioactivity.initial_specific_activity * \
                0.5 ** (elapsed / (
                    self.radioactivity.half_life * 315576e2))  # years to seconds
            # formulas based on "Procedure E1: Point Source" [1, p. 85 et seqq.]
            reduced_activity = volume * self.radioactivity.density * specific_activity / \
                distance ** 2
            return [Radiation(self.name,
                              reduced_activity * self.radioactivity.cf_dose_rate,
                              reduced_activity * self.radioactivity.cf_effective_dose_rate)]

    def get_reduced_radiation(self, incoming, distance):
        """Returns the reduced radiation resulting from the incoming radiation
        travelling distance [cm] through this material.
        """
        if self.hvl is None:
            return incoming
        else:
            hvl_value = self.hvl[incoming.radionuclide]
            ratio = 0.5**(distance / hvl_value)
            return Radiation(incoming.radionuclide, incoming.dose_rate * ratio,
                             incoming.effective_dose_rate * ratio)


class Radioactivity:
    """This class combines interesting properties of radioactive isotopes that
    are needed to estimate the radiation.
    """
    def __init__(self, density, mass_number, half_life, cf_dose_rate, cf_effective_dose_rate):
        """Initialization setting the mass number, half life [y],
        conversion factors for dose rate [(mGy/h)/kBq] and effective dose rate
        [(mSv/h)/kBq].
        """
        self.density = density
        self.mass_number = mass_number
        self.half_life = half_life
        self.cf_dose_rate = cf_dose_rate
        self.cf_effective_dose_rate = cf_effective_dose_rate

        # [kBq/s], formula from "Activity Calculation" [1, p. 121 et seq.]
        self.initial_specific_activity = 1.32e13 / (half_life * mass_number)


class Radiation:
    """This class represents the properties of radiation needed in the
    simulation.
    """
    def __init__(self, radionuclide, dose_rate, effective_dose_rate):
        """Initializes an instance of Radiation setting the source radionuclide,
        dose rate [mGy/h], and effective dose rate [mSv/h] and emitting
        radionuclide.
        """
        self.radionuclide = radionuclide
        self.dose_rate = dose_rate
        self.effective_dose_rate = effective_dose_rate


class Compound:
    """This class represents compound radioactive materials.
    """
    def __init__(self, name, density, components):
        """Sets the name and density of the compound and its components, which
        is a list of tuples (component, mass fraction).
        """
        self.name = name
        self.density = density
        self.components = components
        self.radioactivity = True

    def get_radiation(self, volume, distance):
        """Returns the radiation emitted by a point source with volume [cm^3] of
        this compound transmitted to a point at given distance [m], ignoring any
        shielding effects. None is returned if this material is not radioactive.
        """
        radiation_list = []
        mass = volume * self.density
        for (material_name, fraction) in self.components:
            material = MaterialCatalogue.instance().get_material_by_name(material_name)
            partial_volume = mass * fraction / material.radioactivity.density
            radiation = material.get_radiation(partial_volume, distance)
            if radiation is not None:
                radiation_list.extend(radiation)
        return radiation_list

    def get_reduced_radiation(self, incoming, distance):
        return incoming
