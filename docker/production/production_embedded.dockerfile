# The following Dockerfile is from this Repository that isthe official repository
#  that the arduino community reference for downloading rosserial :
# https://github.com/frankjoshua/rosserial_arduino_lib/blob/master/Dockerfile
# The Official 
FROM ros:noetic-ros-base
# Set the 
ENV ARDUINO_BOARD="arduino:avr:mega"


RUN  /bin/bash -c 'source /opt/ros/noetic/setup.bash && \
    mkdir -p /home/catkin_ws/src && \
    cd /home/catkin_ws/ && \
    catkin_make && \
    source devel/setup.bash'


RUN apt update && apt install -y ros-noetic-rosserial-arduino && rm -rf /var/lib/apt/


RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       gcc \
       curl \
       vim \
       git  && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh |  sh  &&\
    arduino-cli core update-index &&\
    arduino-cli core install arduino:avr



# Installing the latest version of the Rosserial Arduino Library 0.9.4 got me the following error:
#  Therefore I had to install the version 0.7.9 as mentioned in this post.
# https://answers.ros.org/question/361930/rosserial-arduino-compilation-error-no-cstring/

RUN arduino-cli lib install "Rosserial Arduino Library@0.7.9" &&\
    sed -i '/#include "ros\/node_handle.h"/a #include "geometry_msgs/Vector3.h"' /root/Arduino/libraries/Rosserial_Arduino_Library/src/ros.h

RUN arduino-cli lib  install "Servo@1.2.1"
RUN arduino-cli lib install "BlueRobotics MS5837 Library@1.1.1"
WORKDIR /root/Arduino/libraries
# Download the Hydrus_Embedded library from github
RUN git clone https://github.com/Rumarino-Team/sensor_actuator_pkg.git
# COPY ../ ./sensor_actuator_pkg
# Copy entrypoint script
COPY entrypoint.sh /embedded_entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /home/catkin_ws/

ENTRYPOINT ["/embedded_entrypoint.sh"]
CMD ["bash"]