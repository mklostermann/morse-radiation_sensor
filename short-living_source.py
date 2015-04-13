#! /usr/bin/env morseexec

""" Basic MORSE simulation scene the short-living_source environment. Used to
evaluate the correct consideration of the half life.

Run with a command line argument "debug" to connect to the PyCharm remote
debugger (you have to alter the path to the library to match your setup).
"""

from morse.builder import *
from morse.builder.robots.morserobots import ATRV
import math
from nuclear_radiation_sensor.builder.sensors.nuclear_radiation import \
    NuclearRadiation
from nuclear_radiation_sensor.tools.debughelper import RemoteDebugHelper

import sys

if sys.argv[-1] == "debug":
    RemoteDebugHelper(12345, "/opt/pycharm-4.0.4/pycharm-debug.egg").connect()

# add the robot (iRobot ATRV)
robot = ATRV()
robot.set_mass(50.0)
robot.location = (5.0, 0.0, 0.0)
robot.rotate(z=math.pi)

# add a motion controller
motion = MotionVW()
motion.add_stream("ros")
robot.append(motion)
robot.properties(GroundRobot=True)

# add a pose sensor that exports the current location and orientation
# of the robot in the world frame
pose = Pose()
pose.add_stream("ros")
robot.append(pose)

# add the radiation sensor
radiation = NuclearRadiation()
radiation.add_stream("ros", "nuclear_radiation_sensor.middleware.ros.radiation.RadiationPublisher")
radiation.translate(x=0.25, z=0.75)
robot.append(radiation)

# set 'fastmode' to True to switch to wireframe mode
env = Environment('data/environments/short-living_source.blend', fastmode=False)
env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.05, 0, 0.78])
