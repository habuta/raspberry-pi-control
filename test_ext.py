#libraries
import RPi.GPIO as GPIO
from time import sleep
import time

#disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO Mode
GPIO.setmode(GPIO.BCM)
#set red,green and blue pins
redPin = 13
greenPin = 19
bluePin = 26
buzzer_pin = 27
switch_pin = 22
GPIO_TRIG1 = 9 
GPIO_ECHO1 = 10
GPIO_TRIG2 = 23 
GPIO_ECHO2 = 24
#set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(GPIO_TRIG1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN) 
GPIO.setup(GPIO_TRIG2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN) 

#set switch output line as an input
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set up RGB LED for green, red, and yellow



    
def color(red_color, green_color, blue_color):
    GPIO.output(redPin, red_color)
    GPIO.output(greenPin, green_color)
    GPIO.output(bluePin, blue_color)
	
def prox(echo_pin, trig_pin):
        # Send trigger signal
        GPIO.output(trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig_pin, GPIO.LOW) 
        pulse_start = pulse_end = None
        # Measure echo signal
        timeout_start = time.time()
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > 0.1:
                return False

        timeout_start = time.time()
        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()
            if pulse_end - timeout_start > 0.1:
                return False

        # Ensure valid pulse_start and pulse_end values
        if pulse_start is None or pulse_end is None:
            return False
        # Calculate distance in cm
        pulse_duration = pulse_end - pulse_start
        distance_cm = pulse_duration * 17150
        distance_cm = round(distance_cm, 2)
        if distance_cm <= 30:
            return True 
        else: 
            return False

 

try:  
    while True:#000000

        if GPIO.input(switch_pin) == GPIO.LOW:
            color(0, 0, 1)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(3)
            print("red")
            
        elif prox(GPIO_ECHO1, GPIO_TRIG1) or prox(GPIO_ECHO2, GPIO_TRIG2):
            color(0, 1, 1)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            print("yellow")
        
        else:
            color(0, 1, 0)
            GPIO.output(buzzer_pin, GPIO.LOW)
            print("green")
        # Wait for a short time to debounce the switch

  
finally:                     
    GPIO.cleanup()
