#!/usr/bin/env python

import rospy
import sys
import select
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from time import sleep

class Input():

	def __init__(self, max_vel, max_ang):
		rospy.init_node('func_ip')
		self.robot_velocity = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		self.robot = Twist()
		self.robot.linear.x = 0
		self.robot.angular.z = 0

		self.max_vel = max_vel
		self.max_ang = max_ang

		self.location = []


	def publish_result(self):
		self.robot_velocity.publish(self.robot)


	def forward(self, change):
		self.robot.linear.x = (lambda: (lambda: self.robot.linear.x + self.robot.linear.x * change, lambda: self.robot.linear.x - self.robot.linear.x * change)[self.robot.linear.x < 0]() ,
	 lambda: 0.1)[self.robot.linear.x == 0]()
		
		self.robot.linear.x = (lambda: self.robot.linear.x, 
	lambda: self.max_vel)[self.robot.linear.x > self.max_vel]()
		return self.robot.linear.x
		

	def backward(self, change):
		self.robot.linear.x = (lambda: (lambda: self.robot.linear.x - self.robot.linear.x * change, lambda: self.robot.linear.x + self.robot.linear.x * change)[self.robot.linear.x < 0]() ,
	lambda: -0.1)[self.robot.linear.x == 0]()
		
		self.robot.linear.x = (lambda: self.robot.linear.x, 
	lambda: -1 * self.max_vel)[self.robot.linear.x < -1 * self.max_vel]()
		return self.robot.linear.x


	def anticlockwise(self, change):
		self.robot.angular.z = (lambda: (lambda: self.robot.angular.z + self.robot.angular.z * change, lambda: self.robot.angular.z - self.robot.angular.z * change)[self.robot.angular.z < 0]() , 
	lambda: 0.4)[self.robot.angular.z == 0]()

		self.robot.angular.z = (lambda: self.robot.angular.z, 
	lambda: self.max_ang)[self.robot.angular.z > self.max_ang]()
		return self.robot.angular.z


	def clockwise(self, change):
		self.robot.angular.z = (lambda: (lambda: self.robot.angular.z - self.robot.angular.z * change, lambda: self.robot.angular.z - self.robot.angular.z * change)[self.robot.angular.z < 0]() , 
	lambda: -0.4)[self.robot.angular.z == 0]()
		
		self.robot.angular.z = (lambda: self.robot.angular.z, 
	lambda: -1 * self.max_ang)[self.robot.angular.z < -1 * self.max_ang]()
		return self.robot.angular.z

	
	def stop(self):
		self.robot.linear.x = 0
		self.robot.angular.z = 0
		return [0,0]


	def increase_change(self, change):
		return change + 0.1


	def decrease_change(self, change):
		return change - 0.1


	def pos_callback(self, pos):
		self.location = [pos.pose.pose.position.x, pos.pose.pose.position.y, pos.pose.pose.orientation.z]
		self.sub_loc.unregister()


	def set_location(self):
		self.sub_loc = rospy.Subscriber('/odom', Odometry, self.pos_callback)

		if (len(self.location) == 0):
			sleep(0.05)
			return self.set_location()

		return self.location

	
