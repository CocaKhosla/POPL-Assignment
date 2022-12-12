#!/usr/bin/env python

import functional_input
from time import sleep
import select
import sys

# create an instance of the robot
robot_v = functional_input.Input(0.22,2.5)

counter = 10
change = 0.1
forward_vel = 0
angular_vel = 0

for ctr in range(10000):
	if counter == 10:
		print('Press the following Keys and Enter: ')
		print('\t\tW')
		print('\tA\tS\tD')
		print('\t\tX')
		print('to Move Forward, Backwards, Rotate Clockwise, Rotate Anticlockwise, Stop [W, S, A, D, X]')
		print('Also, Q: Precentage Increase Rate of Change of Velocity, E: Percentage Reduce Rate of Change of Velocity')
		counter = 0

	print('Enter Option: '),
	event = select.select([sys.stdin], [], [], 1)[0]
	if event:
		value = sys.stdin.readline().rstrip()

		if value == 'w' or value == 'W':
			forward_vel = robot_v.forward(change)

		if value == 's' or value == 'S':
			forward_vel = robot_v.backward(change)

		if value == 'a' or value == 'A':
			angular_vel = robot_v.anticlockwise(change)

		if value == 'd' or value == 'D':
			angular_vel = robot_v.clockwise(change)

		if value == 'X' or value == 'x':
			(forward_vel, angular_vel) = robot_v.stop()

		if value == 'q' or value == 'Q':
			change = robot_v.increase_change(change)

		if value == 'e' or value == 'E':
			change = robot_v.decrease_change(change)

		robot_v.publish_result()
	else:
		print("")
	print('Linear Velocity: ', str(forward_vel), 'Angular Velcity: ', str(angular_vel), 'Percentage Rate of Change of Velocity:', str(change*100))

