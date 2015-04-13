from morse.builder import Cube
from morse.builder.creator import SensorCreator


class NuclearRadiation(SensorCreator):
    def __init__(self, name=None):
        SensorCreator.__init__(self, name,
                               "nuclear_radiation_sensor.sensors.nuclear_radiation.NuclearRadiation")

        mesh = Cube("SensorCube")
        mesh.scale = (0.016, .028, .01)
        mesh.color(0.8, 0.0, 0.0)
        self.append(mesh)


