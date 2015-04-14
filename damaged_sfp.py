#! /usr/bin/env morseexec

""" A more complex simulation scene, using the damaged_sfp
environment. It consists of destroyed spent fuel element pools with dislocated
fuel elements. The robot is equipped with a nuclear radiation sensor, a
temperature sensor and a laser scanner.

Run with a command line argument "debug" to connect to the PyCharm remote
debugger (you have to alter the path to the library to match your setup).
"""

from morse.builder import *
from morse.builder.robots.morserobots import ATRV
from nuclear_radiation_sensor.builder.sensors.nuclear_radiation import \
    NuclearRadiation
from nuclear_radiation_sensor.tools.debughelper import RemoteDebugHelper

import sys

if sys.argv[-1] == "debug":
    RemoteDebugHelper(12345, "/opt/pycharm-4.0.4/pycharm-debug.egg").connect()

# add the robot (iRobot ATRV)
robot = ATRV()
robot.set_mass(50.0)
# robot.location = (65.0, 15.0, 0.0)
robot.location = (5.0, 5.0, 0.0)

# add a motion controller
motion = MotionVW()
motion.add_stream("ros")
robot.append(motion)
robot.properties(GroundRobot=True)

# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# add a pose sensor that exports the current location and orientation
# of the robot in the world frame
pose = Pose()
pose.add_stream("ros")
robot.append(pose)

# add a laser scanner
laser = Hokuyo()
laser.add_stream("ros")
laser.translate(x=0.6, z=0.3)
laser.properties(Visible_arc=True)
robot.append(laser)

# add a thermometer
thermometer = Thermometer()
thermometer.add_stream("ros", "nuclear_radiation_sensor.middleware.ros.temperature.TemperaturePublisher")
thermometer.alter("", "nuclear_radiation_sensor.modifiers.gaussian_noise.GaussianNoiseModifier",
                fields_std_devs=[("temperature", 0.05)])
thermometer.translate(x=0.2, z=0.75)
robot.append(thermometer)

# add the radiation sensor
radiation = NuclearRadiation()
radiation.add_stream("ros", "nuclear_radiation_sensor.middleware.ros.radiation.RadiationPublisher")
radiation.alter("", "nuclear_radiation_sensor.modifiers.gaussian_noise.GaussianNoiseModifier",
                fields_std_devs=[("dose_rate", 0.05),
                                 ("effective_dose_rate", 0.05)])
radiation.translate(x=0.25, z=0.75)
radiation.frequency(10)
robot.append(radiation)


# set 'fastmode' to True to switch to wireframe mode
env = Environment('data/environments/damaged_sfp.blend', fastmode=False)
env.set_camera_location([20.0, -20.0, 25.0])
env.set_camera_rotation([1.05, 0, 0.78])
