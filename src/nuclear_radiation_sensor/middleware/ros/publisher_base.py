from morse.middleware.ros import ROSPublisher
from nuclear_radiation_sensor.modifiers.gaussian_noise import \
    GaussianNoiseModifier


class ROSPublisherBase(ROSPublisher):
    """Base class for publishers, provides some shared code (get variance from
    modifier).
    """
    def initialize(self):
        self.variance = {}
        ROSPublisher.initialize(self)

    def get_variance(self, ci, field):
        """Get the variance, if only one modifier of type GaussianNoiseModifier
        is used. Otherwise, zero is returned.
        """
        try:
            return self.variance[field]
        except KeyError:
            # the output_modifiers list only contains the methods, use __self__
            # to get the instance
            modifier = ci.output_modifiers[0].__self__ if len(
                ci.output_modifiers) == 1 else None
            if isinstance(modifier, GaussianNoiseModifier):
                self.variance[field] = modifier.get_std_dev(field)**2
            else:
                self.variance[field] = 0.0
        return self.variance[field]