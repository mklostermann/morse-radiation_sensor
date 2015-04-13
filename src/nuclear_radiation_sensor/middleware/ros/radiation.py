import roslib
roslib.load_manifest("sensor_msgs")

from sensor_msgs.msg import Illuminance
from nuclear_radiation_sensor.middleware.ros.publisher_base import \
    ROSPublisherBase


class RadiationPublisher(ROSPublisherBase):
    """ ROS publisher for the nuclear radiation sensor, publishing the radiation
        using an Illuminance message (sensor_msgs/Illuminance.msg).
    """
    ros_class = Illuminance

    def default(self, ci):
        """Publishes an Illuminance message containing the current dose rate and
        the variance (if a Gaussian noise modifier is applied.
        """
        msg = Illuminance()
        msg.header = self.get_ros_header()
        msg.illuminance = self.data["dose_rate"]
        msg.variance = self.get_variance(ci, "dose_rate")

        self.publish(msg)
