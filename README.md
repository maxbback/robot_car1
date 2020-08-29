# robot_car1
Robot car with raspberry pi 3, ultrasonic distance sensor and auto random driving
This robot car is based on a component set from camjam.me/edukit + a raspberry pi 3 and ros2
To make this work you need to install ros2 on your raspberry pi
The robot is able to drive around randomly and avoids walls and big obsticles, however due to the limitation of ultrasonic sensors it hits walls if it is comming driving in an angle to the wall due to ultrasonic echo in this situation return wrong information. Additional sensors can be added, I describe that in another repo robot_car2
All code is written in python, gpio is used for accessing the HW

Project will be complemented with a full guide with pictures etc.
