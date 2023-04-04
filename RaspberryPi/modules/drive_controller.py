import RPi.GPIO as GPIO  #Reuqires Raspberry Pi Platform


""" A Class to Implement Vehicle Control at hardware level on Raspberry PI
"""
class DriveController:
    motorPinout = {
        "FR": [14, 15, 16],
        "FL": [17, 18, 19],
        "RL": [20, 21, 22],
        "RR": [23, 24, 25]
    }

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        self.pwm = {}
        for motor in DriveController.motorPinout:
            pinout = DriveController.motorPinout[motor]
            GPIO.setup(pinout[0], GPIO.OUT)
            GPIO.setup(pinout[1], GPIO.OUT)
            GPIO.setup(pinout[2], GPIO.OUT)
            GPIO.output(pinout[1], GPIO.LOW)
            GPIO.output(pinout[2], GPIO.LOW)
            pwm = GPIO.PWM(pinout[0], 1000)
            pwm.start(25)
            self.pwm[motor] = pwm


    def setForward(self, wheel: str, power: float):
        GPIO.output(DriveController.motorPinout[wheel][1], GPIO.LOW)
        GPIO.output(DriveController.motorPinout[wheel][2], GPIO.HIGH)
        self.pwm[wheel].ChangeDutyCycle(abs(power))


    def setBackward(self, wheel: str, power: float):
        GPIO.output(DriveController.motorPinout[wheel][1], GPIO.HIGH)
        GPIO.output(DriveController.motorPinout[wheel][2], GPIO.LOW)
        self.pwm[wheel].ChangeDutyCycle(abs(power))


    def setInput(self, val):
        left, right = float(val[0]) / 655.35, float(val[1]) / 655.35
        left = max(min(left, 100), -100)  # Clamp the input signals to the range -100 to 100
        right = max(min(right, 100), -100)

        if (left >= 0):
            self.setForward("FL", left)
            self.setForward("RL", left)
        else:
            self.setBackward("FL", left)
            self.setBackward("RL", left)

        if (right >= 0):
            self.setForward("FR", left)
            self.setForward("RR", left)
        else:
            self.setBackward("FR", left)
            self.setBackward("RR", left)