"""This Python module will execute the operation to the D153B module.\n
what you need to give include the wpi number where Standby, AIN, BIN, and PWM are connected.\n
and also the speed you need for two wheels.\n
This module will assume that you will connect left motor to the A channel and right motor to the B channel.\n 
so DO NOT CONNECT TWO MOTORS BACKWARDS! Or you will get something you dont expected.\n
"""
import wiringpi as wpi
from wiringpi import GPIO
import time
import math
import warnings

class d153b:

    def __init__(self,stby:int,a_in1:int,a_in2:int,b_in1:int,b_in2:int,pwm_a:int,pwm_b:int,speed_a:int,speed_b:int):
        self.__version = 1.00
        self._is_running = False
        self.stby = stby
        self.a_in1 = a_in1
        self.a_in2 = a_in2
        self.b_in1 = b_in1
        self.b_in2 = b_in2   
        self.pwm_a = pwm_a
        self.pwm_b = pwm_b
        self.speed_a = speed_a
        self.speed_b = speed_b


    def run(self):

        time_requested = 1 # second(s).

    # do initalize work
        def cleanup():
            wpi.digitalWrite( self.a_in1, GPIO.LOW )
            wpi.digitalWrite( self.a_in2, GPIO.LOW )
            wpi.digitalWrite( self.b_in1, GPIO.LOW )
            wpi.digitalWrite( self.b_in2, GPIO.LOW )
            wpi.digitalWrite( self.stby, GPIO.LOW )
            wpi.pwmWrite( self.pwm_a , 0)
            wpi.pwmWrite( self.pwm_b , 0)


        wpi.wiringPiSetup()
        wpi.pinMode( self.a_in1 , GPIO.OUTPUT ) 
        wpi.pinMode( self.b_in1 , GPIO.OUTPUT )
        wpi.pinMode( self.a_in2 , GPIO.OUTPUT )
        wpi.pinMode( self.b_in2 , GPIO.OUTPUT )
        wpi.pinMode( self.stby , GPIO.OUTPUT )
        wpi.pinMode( self.pwm_a, GPIO.PWM_OUTPUT)
        wpi.pinMode( self.pwm_b, GPIO.PWM_OUTPUT)
        cleanup()

        # Start running as the time requested
        # First, calculate the number pwmWrite should use.

        def speed_processing(speed):
            if isinstance(speed, int) == False:
                print("uh oh... the speed is invalid.")
                cleanup()
                return 1
            elif (speed < -100 or speed > 100 or speed == 0):
                print("uh oh... the speed is OOR.")
                cleanup()
                return 1
            else:
                if speed > 0:
                    direction = True # forward = True, backforward = False
                elif speed < 0:
                    direction = False
            speed_info = {"speed_raw": math.trunc(math.fabs(speed)), "direction": direction}
            return speed_info

        speed_a_raw = speed_processing(self.speed_a)["speed_raw"] * 10
        speed_a_direction = speed_processing(self.speed_a)["direction"]
        speed_b_raw = speed_processing(self.speed_b)["speed_raw"] * 10
        speed_b_direction = speed_processing(self.speed_b)["direction"]

        def spd_direct(direction,group):
            if group == "A":
                if direction == True:
                    wpi.digitalWrite( self.a_in1, GPIO.HIGH )
                    wpi.digitalWrite( self.a_in2, GPIO.LOW )
                elif direction == False:
                    wpi.digitalWrite( self.a_in1, GPIO.LOW )
                    wpi.digitalWrite( self.a_in2, GPIO.HIGH )
            elif group == "B":
                if direction == True:
                    wpi.digitalWrite( self.b_in1, GPIO.HIGH )
                    wpi.digitalWrite( self.b_in2, GPIO.LOW )
                elif direction == False:
                    wpi.digitalWrite( self.b_in1, GPIO.LOW )
                    wpi.digitalWrite( self.b_in2, GPIO.HIGH )

        spd_direct(speed_a_direction,"A")
        spd_direct(speed_b_direction,"B")


        wpi.pwmWrite( self.pwm_a , speed_a_raw)
        wpi.pwmWrite( self.pwm_b , speed_b_raw)
        wpi.digitalWrite( self.stby, GPIO.HIGH )
        self._is_running = True
    

    def stop(self):
        if self._is_running == True:
            wpi.digitalWrite( self.a_in1, GPIO.LOW )
            wpi.digitalWrite( self.a_in2, GPIO.LOW )
            wpi.digitalWrite( self.b_in1, GPIO.LOW )
            wpi.digitalWrite( self.b_in2, GPIO.LOW )
            wpi.digitalWrite( self.stby, GPIO.LOW )
            wpi.pwmWrite( self.pwm_a , 0)
            wpi.pwmWrite( self.pwm_b , 0)
            self._is_running == False
        else :
            warnings.warn("The vehicles is not running!", RuntimeWarning)
