#!/usr/bin/env python

import rospy
import sys
import select
from geometry_msgs.msg import Twist


rospy.init_node('teleoperation_input')

robot_velocity = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10)

robot = Twist()
robot.linear.x = 0
robot.angular.z = 0
change = 0.1
counter = 10
while not rospy.is_shutdown():
	
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
			if robot.linear.x == 0:
				robot.linear.x = 0.1
			else:
				if robot.linear.x > 0:
					robot.linear.x = robot.linear.x + robot.linear.x * change

				else:
					robot.linear.x = robot.linear.x - robot.linear.x * change
				if robot.linear.x >= 0.22:
					robot.linear.x = 0.22

		if value == 's' or value == 'S':
			if robot.linear.x == 0:
				robot.linear.x = -0.1
			else:
				if robot.linear.x > 0:
					robot.linear.x = robot.linear.x - robot.linear.x * change
				else:
					robot.linear.x = robot.linear.x + robot.linear.x * change

				if robot.linear.x < -0.22:
					robot.linear.x = -0.22

		if value == 'a' or value == 'A':
			if robot.angular.z == 0:
				robot.angular.z = -0.1
			else:
				robot.angular.z = robot.angular.z - robot.angular.z * change
				if robot.angular.z < -2.5:
					robot.angular.z = -2.5

		if value == 'd' or value == 'D':
			if robot.angular.z == 0:
				robot.angular.z = 0.1
			else:
				robot.angular.z = robot.angular.z + robot.angular.z * change
				if robot.angular.z > 2.5:
					robot.angular.z = 2.5

		if value == 'X' or value == 'x':
			robot.linear.x = 0
			robot.angular.z = 0

		if value == 'q' or value == 'Q':
			change += 0.1

		if value == 'e' or value == 'E':
			change -= 0.1

	else:
		print("")
	print('Linear Velocity: ', str(robot.linear.x), 'Angular Velcity: ', str(robot.angular.z), 'Percentage Rate of Change of Velocity:', str(change*100))

	robot_velocity.publish(robot)
	counter += 1

	

		
	
		
