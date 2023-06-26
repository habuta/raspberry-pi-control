import RPi.GPIO as GPIO
import time
import os
from packages import send_email, send_message, get_response
from utils import parse_reponse, get_current_video, get_lastn_videos


#disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO Mode
GPIO.setmode(GPIO.BCM)


SERVER_ADDRESS = "http://192.168.43.88:5000"
SAVE_VIDEO_DIR = "temp/stream"
LAST_N = 25
MAX_DIST = 5

# Define GPIO pins
PIN_RED = 13
PIN_GREEN = 19
PIN_BLUE = 26
PIN_BUZZER = 27
PIN_SWITCH = 22
PIN_TRIG1 = 9 
PIN_ECHO1 = 10
PIN_TRIG2 = 23 
PIN_ECHO2 = 24

# Set GPIO pins as outputs
GPIO.setup(PIN_RED, GPIO.OUT)
GPIO.setup(PIN_GREEN, GPIO.OUT)
GPIO.setup(PIN_BLUE, GPIO.OUT)
GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.setup(PIN_TRIG1, GPIO.OUT)
GPIO.setup(PIN_ECHO1, GPIO.IN) 
GPIO.setup(PIN_TRIG2, GPIO.OUT)
GPIO.setup(PIN_ECHO2, GPIO.IN)

# Set switch output line as an input
GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def color(red_color, green_color, blue_color):
    GPIO.output(PIN_RED, red_color)
    GPIO.output(PIN_GREEN, green_color)
    GPIO.output(PIN_BLUE, blue_color)

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
        if pulse_start - timeout_start > 0.5:
            return False

    timeout_start = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
        if pulse_end - timeout_start > 0.5:
            return False
        
    if pulse_start is None or pulse_end is None:
        return False

    return round((pulse_end - pulse_start) * 17150, 2) <= MAX_DIST

def main():
    # Set initial color to green
    color(0, 1, 0)

    switch_state = False
    prox1_state = False
    prox2_state = False
    email_state = True
    message_state = False
    video_state = False

    last_motion_type = None
    motion_stack = []

    while True:
        # set color to green
        switch_state = GPIO.input(PIN_SWITCH) is GPIO.LOW
        video_state = False
        prox1_state = False
        prox2_state = False

        if switch_state:
            color(0, 0, 1)

        else:
            prox1_state = prox(PIN_ECHO1, PIN_TRIG1)
            prox2_state = prox(PIN_ECHO2, PIN_TRIG2)

            if prox1_state or prox2_state:
                color(0, 1, 1)

            else:
                video_name = get_current_video()
                print(video_name, f"{SAVE_VIDEO_DIR}/{video_name}", os.path.exists(f"{SAVE_VIDEO_DIR}/{video_name}"))
                if os.path.exists(f"{SAVE_VIDEO_DIR}/{video_name}"):

                    try:
                        response = get_response(f"{SAVE_VIDEO_DIR}/{video_name}", SERVER_ADDRESS)
                        predictions = parse_reponse(response)
                        print(predictions)

                        last_motion_type = predictions[0]

                        if last_motion_type != "Normal":
                            video_state = True
                            color(0, 1, 1)
                    except Exception as e:
                        print("error 1:", e)
                        
                else:
                    color(0, 1, 0)

        # print all states
        print(
            f"switch_state = {switch_state}, prox1_state = {prox1_state}, prox2_state = {prox2_state}, video_state = {video_state}"
        ) 
        if switch_state or prox1_state or prox2_state or video_state:
            if email_state:
                last_n_videos = get_lastn_videos(LAST_N)
                os.system(f"cat {' '.join([SAVE_VIDEO_DIR + '/' + i for i in last_n_videos])} > {SAVE_VIDEO_DIR}/concat.mp4")
                send_email("Suspicious activity detected. Please check the attached video", f"{SAVE_VIDEO_DIR}/concat.mp4")
            if message_state:
                send_message(f"{SAVE_VIDEO_DIR}/{video_name}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
