cmake_minimum_required(VERSION 3.0.2)
project(capstone_fyp)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
  # INCLUDE_DIRS include
  # LIBRARIES capstone_fyp
  CATKIN_DEPENDS rospy std_msgs
  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
catkin_install_python(PROGRAMS
  scripts/chatbot/chatbot_function_node_clean.py
  scripts/noise_level_detection/noise_detection_clean.py
  scripts/chatbot/chatbot_main_clean.py
  scripts/chatbot/chatbot_function_node_clean_without_mic.py
  scripts/face_detection/face_detection_clean.py
  # scripts/simple_pub_and_sub_test/listener.py
  # scripts/face_detection/face_detection.py
  # scripts/noise_level_detection/noise_detection_pub_sub.py
  # scripts/chatbot/chatbot.py
  # scripts/noise_level_detection/noise_detection_pub_sub2.py
  # scripts/noise_level_detection/noise_detection.py
  # scripts/noise_level_detection/noise_detection_2021-11-09_1318.py
  # scripts/chatbot/chatbot_function_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)