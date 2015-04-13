#! /usr/bin/env morseexec

""" First simple simulation built on top of the default MORSE template
(default.py) to allow basic tests.

Run with a command line argument "debug" to connect to the PyCharm remote
debugger (you have to alter the path to the library to match your setup).
"""

from morse.builder import *
from nuclear_radiation_sensor.builder.sensors.nuclear_radiation import NuclearRadiation
from nuclear_radiation_sensor.tools.debughelper import RemoteDebugHelper

import sys

if sys.argv[-1] == "debug":
    RemoteDebugHelper(12345, "/opt/pycharm-4.0.4/pycharm-debug.egg").connect()

# Add the MORSE mascott, MORSY.
# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> nuclear_radiation_sensor' can help you to build custom robots.
robot = ATRV()

# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
robot.translate(5.0, 5.0, 0.0)

# Add a motion controller
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
#
# 'morse add actuator <name> nuclear_radiation_sensor' can help you with the creation of a custom
# actuator.
motion = MotionVW()
robot.append(motion)

# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#sensors
#
# 'morse add sensor <name> nuclear_radiation_sensor' can help you with the creation of a custom
# sensor.
pose = Pose()
robot.append(pose)

# MY STUFF
radiation = NuclearRadiation()
robot.append(radiation)

# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html 
# the other available interfaces (like ROS, YARP...)
robot.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
env = Environment('data/environments/simple.blend', fastmode = False)
env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.05, 0, 0.78])
