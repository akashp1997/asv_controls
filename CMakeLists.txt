cmake_minimum_required(VERSION 2.8.3)
project(asv_controls)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  nav_msgs
  asv_localization
  pid
  geometry_msgs
  sensor_msgs
)

catkin_package(  
	CATKIN_DEPENDS 
  rospy
  std_msgs
  nav_msgs
  asv_localization
  pid
  geometry_msgs
  sensor_msgs
)