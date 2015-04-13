import logging
logger = logging.getLogger("morse." + __name__)
import random

from morse.helpers.components import add_property
from morse.modifiers.abstract_modifier import AbstractModifier


class GaussianNoiseModifier(AbstractModifier):
    """This generic modifier allows to simulate Gaussian noise for float
    measurements.
    """

    add_property("fields_std_devs", None, "fields_std_devs", "list",
                 "List containing tuples (data field name, standard deviation) for all data fields that shall be modified.")

    def initialize(self):
        """Initialization of the modifier (does some logging)."""
        self.fields_std_devs = self.parameter("fields_std_devs")
        log_string = ""
        for (field, std_dev) in self.fields_std_devs:
            log_string += field + " (" + str(std_dev) + "), "
        logger.info(
            "Initialized gaussian noise modifier for following data fields, standard deviation in parentheses: %s",
            log_string)

    def modify(self):
        """Modifies the values of configured fields using Gaussian noise with
        the configured standard deviation.
        """
        for (field, std_dev) in self.fields_std_devs:
            value = self.data[field]
            modified_value = random.gauss(value, std_dev)
            logger.debug("Modifying %s from %f to %f", field, value,
                         modified_value)
            self.data[field] = modified_value

    def get_std_dev(self, field):
        """Returns the standard deviation applied to given field or 0 if no
        noise is applied.
        """
        for (field_name, std_dev) in self.fields_std_devs:
            if field_name == field:
                return std_dev
        return 0.0