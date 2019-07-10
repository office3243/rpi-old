import lcddriver
import RPi.GPIO as GPIO
import time


lcd = lcddriver.lcd()
while True:
    lcd.lcd_display_string('Print My Copy', 1)
    lcd.lcd_display_string('Test For LCD 12345', 2)
    lcd.lcd_clear()
    time.sleep(1)
