import roslib
roslib.load_manifest("sensor_msgs")

from sensor_msgs.msg import Temperature
from nuclear_radiation_sensor.middleware.ros.publisher_base import \
    ROSPublisherBase


class TemperaturePublisher(ROSPublisherBase):
    """ ROS publisher for the thermometer sensor, publishing the temperature
        using a temperature message (sensor_msgs/Temperature.msg).
    """
    ros_class = Temperature

    def default(self, ci):
        """Publishes an Temperature message containing the current temperature
        and the variance (if a Gaussian noise modifier is applied.
        """
        msg = Temperature()
        msg.header = self.get_ros_header()
        msg.temperature = self.data["temperature"]
        msg.variance = self.get_variance(ci, "temperature")
        self.publish(msg)