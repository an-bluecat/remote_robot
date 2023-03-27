import RPi.GPIO as GPIO
from time import sleep
import math as m

""" A Class to Implement Vehicle Control at hardware level on Raspberry PI
"""


GPIO.setmode(GPIO.BCM)

# motor 1
in1 = 14
in2 = 15
en1 = 18

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1=GPIO.PWM(en1,1000)
p1.start(25)


# motor 2
in3 = 23
in4 = 24
en2 = 25

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2,1000)
p2.start(25)

# motor 3
in5 = 17
in6 = 27
en3 = 22

GPIO.setup(in5,GPIO.OUT)
GPIO.setup(in6,GPIO.OUT)
GPIO.setup(en3,GPIO.OUT)
GPIO.output(in5,GPIO.LOW)
GPIO.output(in6,GPIO.LOW)
p3=GPIO.PWM(en3,1000)
p3.start(25)

# motor 4
in7 = 10
in8 = 9
en4 = 11

GPIO.setup(in7,GPIO.OUT)
GPIO.setup(in8,GPIO.OUT)
GPIO.setup(en4,GPIO.OUT)
GPIO.output(in7,GPIO.LOW)
GPIO.output(in8,GPIO.LOW)
p4=GPIO.PWM(en4,1000)
p4.start(25)


def control_speed(self, speed):
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)
    p3.ChangeDutyCycle(speed)
    p4.ChangeDutyCycle(speed)

def DriveController():
    def __init__(self):
        """
        set x,y as the position of joystick controller
        Moving Direction
            left -- x
        motor_pin_list -- given 4 motors pin position on Rasp pi,
                         for every motor, there are 3 parameter [signal1, signal2, enable speed signal]
        """

    def update_motors(self, x, y):
        if x == 0 and y == 0:
            control_speed(0)
        if x > y: # turn left or right
            if x > 0: # right
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
                GPIO.output(in5, GPIO.HIGH)
                GPIO.output(in6, GPIO.LOW)
                GPIO.output(in7, GPIO.LOW)
                GPIO.output(in8, GPIO.HIGH)
                control_speed(x)
            elif x < 0: # left
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
                GPIO.output(in5, GPIO.LOW)
                GPIO.output(in6, GPIO.HIGH)
                GPIO.output(in7, GPIO.HIGH)
                GPIO.output(in8, GPIO.LOW)
                control_speed(-x)
        elif x < y:
            if y > 0: # up
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
                GPIO.output(in5, GPIO.HIGH)
                GPIO.output(in6, GPIO.LOW)
                GPIO.output(in7, GPIO.HIGH)
                GPIO.output(in8, GPIO.LOW)
                control_speed(y)
            elif y < 0: # down
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
                GPIO.output(in5, GPIO.LOW)
                GPIO.output(in6, GPIO.HIGH)
                GPIO.output(in7, GPIO.LOW)
                GPIO.output(in8, GPIO.HIGH)
                control_speed(-y)

    # def init_motor_pin_signal(self):
    #     GPIO.setmode(GPIO.BCM)
    #
    #     # initial signal output on raspberry
    #     for motor in self.motor_pin_list:
    #         GPIO.setup(motor[0], GPIO.OUT)
    #         GPIO.setup(motor[1], GPIO.OUT)
    #         GPIO.output(motor[0], GPIO.LOW)
    #         GPIO.output(motor[1], GPIO.LOW)
    #
    #         GPIO.setup(motor[2], GPIO.OUT)
    #         p = GPIO.PWM(motor[2], 1000)
    #         p.start(0)
    #         self.motor_speed.append(p)
    #
    # def change_motor_power_signal(self, s1, s2):
    #     for motor in self.motor_pin_list:
    #         GPIO.output(motor[0], s1)
    #         GPIO.output(motor[1], s2)
    #
    # def change_motor_speed(self, x, y):
    #     # self.motor_speed[0].ChangeDutyCycle(x)
    #     # self.motor_speed[1].ChangeDutyCycle(y)
    #     # self.motor_speed[2].ChangeDutyCycle(x)
    #     # self.motor_speed[3].ChangeDutyCycle(y)
    #
    #     if y > 0 and x > 0: # up right






        #
        # interval = 5
        # if y > 0 and x >0: # up + right
        #     change_motor_power_signal(self, GPIO.HIGH, GPIO.LOW)
        #
        #
        # # update new speed
        # self.change_motor_speed(x, y)
        #
        # # update a new direction power
        # interval = 5
        # if y >= 0: # up
        #     if x in [-interval, interval]: # up
        #         self.change_motor_power_signal(self, GPIO.HIGH, GPIO.LOW)
        #
        #     elif x > interval: # up and right


    def __del__(self):
        for m_speed in self.motor_speed:
            m_speed.stop()
        GPIO.cleanup()

    def setMaxThrottle(self, *args) -> None:  # Note: THESE ARE PLACEHOLDERS, to be implemented
        pass

    def setInput(self, *args) -> None:
        pass

