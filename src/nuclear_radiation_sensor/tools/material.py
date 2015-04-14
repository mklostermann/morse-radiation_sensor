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
[4] "Fukushima Accident: Radioactivity Impact on the Environment", Pavel
    Povinec, Katsumi Hirose and Michio Aoyama, ISBN: 978-0-12-408132-1
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
        # mass fractions from [4, p. 38]
        self._material = {"24Na": Material("24Na", None,
                                           Radioactivity(0.969, 24,
                                                         14.659/8766, 5.1e-7,
                                                         3.8e-7)),
                          "54Mn": Material("54Mn", None,
                                           Radioactivity(7.43, 54, 312.2/365.25,
                                                         1.5e-07, 8.6e-08)),
                          "60Co": Material("60Co", None,
                                           Radioactivity(8.9, 60, 5.27,
                                                         3.6E-07, 2.5E-07)),
                          "85Kr": Material("85Kr", None,
                                           Radioactivity(2.6, 85, 10.70,
                                                         3.6E-10, 2.3E-10)),
                          "89Sr": Material("89Sr", None,
                                           Radioactivity(2.54, 89, 50.5/365.25,
                                                         2.1E-11, 1.4E-11)),
                          "99Mo": Material("99Mo", None,
                                           Radioactivity(10.20, 99, 66.02/8766,
                                                         2.6E-08, 1.6E-08)),
                          "99mTc": Material("99mTc", None,
                                           Radioactivity(11.48, 99, 6/8766,
                                                         3.0E-08, 1.2E-08)),
                          "110mAg": Material("110mAg", None,
                                           Radioactivity(10.48, 110, 252/365.25,
                                                         4.2E-07, 2.8E-07)),
                          "129mTe": Material("129mTe", None,
                                           Radioactivity(6.23, 129, 33.52/365.25,
                                                         7.8E-08, 4.6E-08)),
                          "131I": Material("131I", None,
                                           Radioactivity(4.92, 131, 8.04/365.25,
                                                         6.2E-08, 3.9E-08)),
                          "132Te": Material("132Te", None,
                                           Radioactivity(6.23, 132, 78.2/365.25,
                                                         4.9E-08, 2.3E-08)),
                          "133I": Material("133I", None,
                                           Radioactivity(4.92, 133, 20.9/8766,
                                                         9.8E-08, 6.2E-08)),
                          "133Xe": Material("133Xe", None,
                                           Radioactivity(3.52, 133, 5.245/365.25,
                                                         1.9E-08, 4.6E-09)),
                          "134Cs": Material("134Cs", None,
                                           Radioactivity(1.870, 134, 2.062,
                                                         2.5E-07, 1.6E-07)),
                          "136Cs": Material("136Cs", None,
                                           Radioactivity(1.870, 136, 13.16/365.25,
                                                         3.4E-07, 2.2E-07)),
                          "144Ce": Material("144Ce", None,
                                           Radioactivity(6.637, 144, 284.5/365.25,
                                                         1.1E-08, 3.1E-09)),
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
                          "241Am": Material("241Am", None,
                                            Radioactivity(13.64, 241, 432,
                                                          3.7E-08, 3.1E-09)),
                          "242Cm": Material("242Cm", None,
                                            Radioactivity(13.49, 242, 162.76/365.25,
                                                          9.2E-09, 3.1E-10)),
                          "242Pu": Material("242Pu", None,
                                            Radioactivity(19.80, 242, 3.73e5,
                                                          6.9e-9, 2.3e-10)),
                          "244Cm": Material("244Cm", None,
                                            Radioactivity(13.49, 244, 18.09,
                                                          8.2E-09, 2.8E-10)),
                          "UOX-4.5": Compound("UOX-4.5", 10.3,
                                              [("235U", 0.045),
                                               ("238U", 0.955)]),
                          "Spent-Fuel": Compound("Spent-Fuel", 10.3,
                                                 [("54Mn", 3.346E-7),
                                                  ("60Co", 8.982E-6),
                                                  ("85Kr", 2.364e-5),
                                                  ("89Sr", 1.889e-5),
                                                  ("99Mo", 2.141e-6),
                                                  ("99mTc", 1.710e-7),
                                                  ("110mAg", 3.420e-7),
                                                  ("129mTe", 5.859e-7),
                                                  ("131I", 4.357e-6),
                                                  ("132Te", 2.543e-6),
                                                  ("133I", 1.007e-6),
                                                  ("133Xe", 5.800e-6),
                                                  ("134Cs", 5.919e-5),
                                                  ("136Cs", 2.989e-7),
                                                  ("144Ce", 1.680e-4),
                                                  ("235U", 1.651e-2),
                                                  ("238U", 9.711e-1),
                                                  ("238Pu", 1.086e-4),
                                                  ("239Pu", 4.536e-3),
                                                  ("240Pu", 1.561e-3),
                                                  ("241Am", 6.573e-5),
                                                  ("242Cm", 1.083e-5),
                                                  ("244Cm", 1.344e-5)]),
                          "Lead": Material("Lead",
                                           {"24Na": 1.32,
                                            "54Mn": 0.68,
                                            "60Co": 1,
                                            "85Kr": 0.41,
                                            "89Sr": 0.74,
                                            "99Mo": 0.49,
                                            "99mTc": 0.49,
                                            "110mAg": 0.71,
                                            "129mTe": 0.38,
                                            "131I": 0.25,
                                            "132Te": 0.1,
                                            "133I": 0.47,
                                            "133Xe": 0.03,
                                            "134Cs": 0.57,
                                            "136Cs": 0.65,
                                            "144Ce": 0.05,
                                            "235U": 0.09,
                                            "238U": 0.01,
                                            "238Pu": 0.01,
                                            "239Pu": 0.01,
                                            "240Pu": 0.01,
                                            "241Am": 0.02,
                                            "242Cm": 0.01,
                                            "242Pu": 0.01,
                                            "244Cm": 0.01}, None),
                          "Iron": Material("Iron",
                                           {"24Na": 2.14,
                                            "54Mn": 1.33,
                                            "60Co": 1.66,
                                            "85Kr": 1.07,
                                            "89Sr": 1.4,
                                            "99Mo": 1.11,
                                            "99mTc": 1.11,
                                            "110mAg": 1.38,
                                            "129mTe": 0.82,
                                            "131I": 0.93,
                                            "132Te": 0.53,
                                            "133I": 1.15,
                                            "133Xe": 0.16,
                                            "134Cs": 1.24,
                                            "136Cs": 1.32,
                                            "144Ce": 0.28,
                                            "235U": 0.46,
                                            "238U": 0.04,
                                            "238Pu": 0.04,
                                            "239Pu": 0.04,
                                            "240Pu": 0.04,
                                            "241Am": 0.12,
                                            "242Cm": 0.01,
                                            "242Pu": 0.04,
                                            "244Cm": 0.04}, None),
                          "Water": Material("Water",
                                            {"24Na": 14.75,
                                             "54Mn": 9,
                                             "60Co": 10.99,
                                             "85Kr": 7.59,
                                             "89Sr": 9.35,
                                             "99Mo": 7.6,
                                             "99mTc": 7.6,
                                             "110mAg": 9.36,
                                             "129mTe": 5.65,
                                             "131I": 6.5,
                                             "132Te": 3.66,
                                             "133I": 8.05,
                                             "133Xe": 1.11,
                                             "134Cs": 8.5,
                                             "136Cs": 8.66,
                                             "144Ce": 1.95,
                                             "235U": 3.19,
                                             "238U": 0.27,
                                             "238Pu": 0.27,
                                             "239Pu": 0.29,
                                             "240Pu": 0.27,
                                             "241Am": 0.82,
                                             "242Cm": 0.28,
                                             "242Pu": 0.27,
                                             "244Cm": 0.28}, None),
                          "Air": Material("Air",
                                          {"24Na": 1.27e4,
                                           "54Mn": 7.7e3,
                                           "60Co": 9.42e3,
                                           "85Kr": 6.31e3,
                                           "89Sr": 8.05e3,
                                           "99Mo": 6.48e3,
                                           "99mTc": 6.48e3,
                                           "110mAg": 7.98e3,
                                           "129mTe": 4.79e3,
                                           "131I": 5.59e3,
                                           "132Te": 3.22e3,
                                           "133I": 6.74e3,
                                           "133Xe": 9.8e3,
                                           "134Cs": 7.19e3,
                                           "136Cs": 7.62e3,
                                           "144Ce": 2.23e3,
                                           "235U": 2.81e3,
                                           "238U": 2.36e2,
                                           "238Pu": 2.37e2,
                                           "239Pu": 2.58e2,
                                           "240Pu": 2.37e2,
                                           "241Am": 7.27e2,
                                           "242Cm": 2.48e2,
                                           "242Pu": 2.37e2,
                                           "244Cm": 2.47e2}, None),
                          "Concrete": Material("Concrete",
                                               {"24Na": 6.88,
                                                "54Mn": 4.22,
                                                "60Co": 5.2,
                                                "85Kr": 3.43,
                                                "89Sr": 4.42,
                                                "99Mo": 3.54,
                                                "99mTc": 3.54,
                                                "110mAg": 4.38,
                                                "129mTe": 2.61,
                                                "131I": 3.02,
                                                "132Te": 1.73,
                                                "133I": 3.67,
                                                "133Xe": 0.53,
                                                "134Cs": 3.93,
                                                "136Cs": 4.18,
                                                "144Ce": 0.93,
                                                "235U": 1.51,
                                                "238U": 0.13,
                                                "238Pu": 0.13,
                                                "239Pu": 0.14,
                                                "240Pu": 0.13,
                                                "241Am": 0.39,
                                                "242Cm": 0.13,
                                                "242Pu": 0.13,
                                                "244Cm": 0.13}, None)}

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
        try:
            return self._material[bge_object["Material"]]
        except KeyError:
            raise KeyError("No 'Material' set for object with name: "+
                           bge_object.name)

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
        """Initialization setting the mass number, half life [a],
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
