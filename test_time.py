#!/usr/bin/env python

import functional_input
from time import sleep

# we want to move the robot straight for 10 seconds and then anticlockwise for 10 seconds

# create an instance of the robot
robot_v = functional_input.Input(0.22, 1.8)
# first tell the robot to move forward
forward_vel = robot_v.forward(0.1)

for counter in range(200):
	# at t = 5s, tell robot to turn clockwise
	if counter == 100:
		angular_vel = robot_v.anticlockwise(0.1)
	robot_v.publish_result()
	sleep(0.1)

loc_set = robot_v.set_location()
# print(robot_v.get_location())
print(loc_set)

