import RPi.GPIO as GPIO
import time

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
    pulse = GPIO.input(13)
    if pulse == 0:
        print(pulse)
        time.sleep(0.5)