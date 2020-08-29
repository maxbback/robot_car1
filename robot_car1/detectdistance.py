# Copyright 2020 SmsTid AB.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

#from tutorial_interfaces.msg import Num

import RPi.GPIO as gpio
import time
import sys
import signal
from std_msgs.msg import Int32


def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class FrontDistanceSensor(Node):

    def __init__(self):
        super().__init__('frontdistancesensor')
        self.frontpublisher = self.create_publisher(Int32, 'frontdistance', 1)
        self.leftpublisher = self.create_publisher(Int32, 'leftdistance', 1)
        self.rightpublisher = self.create_publisher(Int32, 'rightdistance', 1)
        self.distancepublisher = self.create_publisher(Int32, 'distance', 1)
        self.directionpublisher = self.create_publisher(Int32, 'direction', 1)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        gpio.setmode(gpio.BCM)
        self.frontTrig = 17 # 7th
        self.frontEcho = 18 # 6th
        self.leftTrig = 27 # 7th
        self.leftEcho = 22 # 6th
        self.rightTrig = 23 # 7th
        self.rightEcho = 24 # 6th

        self.stopDirection = 0
        self.leftDirection = 1
        self.rightDirection = 2
        self.forwardDirection = 3
        self.backwardDirection = 4

        gpio.setup(self.frontTrig, gpio.OUT)
        gpio.setup(self.frontEcho, gpio.IN)
        gpio.setup(self.leftTrig, gpio.OUT)
        gpio.setup(self.leftEcho, gpio.IN)
        gpio.setup(self.rightTrig, gpio.OUT)
        gpio.setup(self.rightEcho, gpio.IN)

    def getDistance(selv,trigPin,echoPin):
        #time.sleep(0.1)
        time.sleep(0.1)
        gpio.output(trigPin, gpio.HIGH)
        time.sleep(0.00001)
        #0.1 100ms
        #0.01 10ms
        #0.001 1ms
        #0.0001 100 mis
        #0.00001 10 mis
        gpio.output(trigPin, gpio.LOW)
        while gpio.input(echoPin) == gpio.LOW :
            pulse_start = time.time()
        while gpio.input(echoPin) == gpio.HIGH :
            pulse_end = time.time()
        gpio.output(trigPin, gpio.LOW)
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17160
        self.get_logger().info('pulse: "%f"' % pulse_duration)
        if pulse_duration >=0.01746:
            #print('time out')
            msg.data = -1
        elif distance > 300 or distance==0:
            #print('out of range')
            msg.data = -1
        distance = round(distance)
        return distance

    def timer_callback(self):
        msg = Int32()


        gpio.output(self.frontTrig, gpio.LOW)
        gpio.output(self.lefTrig, gpio.LOW)
        gpio.output(self.rightTrig, gpio.LOW)

        frontDistance = self.getDistance(self.frontTrig,self.frontEcho)
        leftDistance = self.getDistance(self.leftTrig,self.leftEcho)
        rightDistance = self.getDistance(self.rightTrig,self.rightEcho)

        msg.data = frontDistance
        self.frontpublisher.publish(msg)
        msg.data = leftDistance
        self.leftpublisher.publish(msg)
        msg.data = rightDistance
        self.rightpublisher.publish(msg)
        distance = frontDistance
        direction = self.backwardDirection # go backward
        if distance < 0 or distance > leftDistance:
            distance = leftDistance
            direction = self.rightDirection # go right
        if distance < 0 or distance > rightDistance:
            distance = rightDistance
            direction = self.leftDirection # go left

        msg.data = distance
        self.distancepublisher.publish(msg)
        if distance < 14:
            msg.data = direction
        else:
            msg.data = self.forwardDirection
        self.directionpublisher.publish(msg)

        msg.data = distance
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data)



def main(args=None):
    rclpy.init(args=args)

    frontsensor = FrontDistanceSensor()

    rclpy.spin(frontsensor)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    frontsensor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
