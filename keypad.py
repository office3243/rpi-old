import RPi.GPIO as GPIO


keyboard_matrix = [['1', '2', '3', 'A', 'E', 'CNL'],
                   ['4', '5', '6', 'B', 'F', 'CLR'],
                   ['7', '8', '9', 'C', 'G', 'DEL'],
                   ['*', '0', '#', "D", 'H', 'ENT']]

row = [37, 35, 33, 31]
col = [29, 40, 38, 36, 32, 26]
for j in range(6):
    GPIO.setup(col[j], GPIO.OUT)
    GPIO.output(col[j], 1)
for i in range(4):
    GPIO.setup(row[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    while True:
        for j in range(5):
            GPIO.output(col[j], 0)
            for i in range(4):
                if GPIO.input(row[i]) == 0:
                    number = keyboard_matrix[i][j]
                    print(number)
                    while GPIO.input(row[i]) == 0:
                        pass
            GPIO.output(col[j], 1)
except KeyboardInterrupt:
    GPIO.cleanup()

