##import os
##try:
##    from PIL import Image
##except:
##    os.mkdir("/home/pi/Desktop/PIL")
##try:
##    import subprocess
##except:
##    os.mkdir("/home/pi/Desktop/SUBP")
##try:
##    import urllib
##except:
##    os.mkdir("/home/pi/Desktop/URLLIB")
##try:
##    import requests
##except:
##    os.mkdir("/home/pi/Desktop/REQUEST")
##try:
##    import time
##except:
##    os.mkdir("/home/pi/Desktop/TIME")
##try:
##    import lcddriver
##except:
##    os.mkdir("/home/pi/Desktop/LCDRIVER")
##try:
##    import RPi.GPIO as GPIO
##except:
##    os.mkdir("/home/pi/Desktop/GPIO")
##try:
##    import cups
##except:
##    os.mkdir("/home/pi/Desktop/CUPS")
##
##



from PIL import Image
import subprocess
import urllib
import requests
import time
import lcddriver
import RPi.GPIO as GPIO
import time
import cups
import os


lcd = lcddriver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string('   Loading...', 1)
# subprocess.call('lpoptions -d l130', shell=True)
conn = cups.Connection()
conn.cancelAllJobs("l130")
GPIO.setmode(GPIO.BOARD)


class Printer:

    def __init__(self):
        self.code = 1234
        self.path = '/home/pi/printer/'
        self.http_url = 'http://www.printmycopy.com'
        # self.http_url = 'http://192.168.0.108:8000'
        self.secret_code = "1515"
        self.printer = "l130"

    def error_message(self):
        lcd.lcd_clear()
        lcd.lcd_display_string('Getting Issues', 1)
        lcd.lcd_display_string('Please Try Again', 2)
        time.sleep(5)
        self.take_otp()

    def check_local_ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        lcd.lcd_clear()
        lcd.lcd_display_string('LOCAL IP : ', 1)
        lcd.lcd_display_string(str(local_ip), 2)
        s.close()
        time.sleep(7)
        self.take_otp()

    def take_otp(self):
        print('take_otp')
        otp_1 = ''
        otp_2 = ''
        lcd.lcd_clear()
        lcd.lcd_display_string('OTP 1 : ', 1)
        lcd.lcd_display_string('OTP 2 : ', 2)

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
                            if number == 'ENT':
                                if len(otp_1) == 4 and len(otp_2) == 4:
                                    if otp_1 == otp_2 == self.secret_code:
                                        self.check_local_ip()
                                    else:
                                        self.request_otp(otp_1, otp_2)
                                else:
                                    pass
                            elif number == 'DEL':
                                if len(otp_2) == 0 and len(otp_1) > 0:
                                    otp_1 = otp_1[:-1]
                                    lcd.lcd_clear()
                                    lcd.lcd_display_string(('OTP 1 : ' + otp_1), 1)
                                    lcd.lcd_display_string(('OTP 2 : ' + otp_2), 2)
                                elif len(otp_1) == 4 and len(otp_2) > 0:
                                    otp_2 = otp_2[:-1]
                                    lcd.lcd_clear()
                                    lcd.lcd_display_string(('OTP 1 : ' + otp_1), 1)
                                    lcd.lcd_display_string(('OTP 2 : ' + otp_2), 2)
                                else:
                                    pass
                            elif number == 'CLR':
                                otp_1 = ""
                                otp_2 = ""
                                lcd.lcd_clear()
                                lcd.lcd_display_string(('OTP 1 : ' + otp_1), 1)
                                lcd.lcd_display_string(('OTP 2 : ' + otp_2), 2)
                            elif number in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                                if len(otp_1) < 4 and len(otp_2) == 0:
                                    otp_1 += number
                                    lcd.lcd_display_string(('OTP 1 : ' + otp_1), 1)
                                    lcd.lcd_display_string(('OTP 2 : ' + otp_2), 2)
                                elif len(otp_1) == 4 and len(otp_2) < 4:
                                    otp_2 += number
                                    lcd.lcd_display_string(('OTP 1 : ' + otp_1), 1)
                                    lcd.lcd_display_string(('OTP 2 : ' + otp_2), 2)
                                else:
                                    pass
                            else:
                                pass
                            while GPIO.input(row[i]) == 0:
                                pass
                    GPIO.output(col[j], 1)
        except KeyboardInterrupt:
            GPIO.cleanup()

    def request_otp(self, otp_1, otp_2):
        lcd.lcd_clear()
        lcd.lcd_display_string('  Please Wait..', 2)
        print("rquest otp")
        try:
            url = '{http_url}/getprint/{otp_1}/{otp_2}/'.format(http_url=self.http_url, otp_1=otp_1, otp_2=otp_2)
            response = requests.get(url)
            response_dict = response.json()
            response.close()
            print(url)
            if not response_dict['otp_found']:
                print("wrong otp")
                lcd.lcd_clear()
                lcd.lcd_display_string('   Wrong OTP ', 2)
                time.sleep(3)
                self.take_otp()
            elif response_dict['otp_found']:
                print("otp found")
                link_text = self.http_url + response_dict["file_path"]
                print(link_text)
                ext = link_text[link_text.rfind('.'):]
                file_name = 'file_tobe_print' + ext
                color_mode = response_dict['color_model']
                payment_mode = response_dict['payment_mode']
                amount = response_dict['amount']
                urllib.request.urlretrieve(link_text, file_name)
                if payment_mode == 'Coin':
                    coin_accepted = self.accept_coin(amount)
                    if coin_accepted:
                        self.take_print(file_name, color_mode)
                    else:
                        self.error_message()
                elif payment_mode == 'Account':
                    self.take_print(file_name, color_mode)
                else:
                    self.error_message()
            else:
                print("url not  found")
                self.error_message()
        except Exception as e:
            print("REQUEST OTP EXCEPTION")
            print(e)
            self.error_message()

    def accept_coin(self, amount):
        try:
            lcd.lcd_clear()
            lcd.lcd_display_string('Put {0} rs'.format(amount), 1)
            lcd.lcd_display_string('in Coinbox', 2)
            input_amount = 0
            GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            while input_amount < amount:
                pulse = GPIO.input(13)
                if pulse == 0:
                    input_amount += 1
                    lcd.lcd_clear()
                    lcd.lcd_display_string(str(amount), 1)
                    lcd.lcd_display_string(str(input_amount), 2)
                    time.sleep(0.5)
            else:
                return True
        except:
            self.error_message()

    def png_to_jpg(self, file_name):
        jpg_file = file_name[:file_name.find('.')] + '.jpg'
        png_file = Image.open(file_name)
        bground = Image.new('RGB', png_file.size, (255, 255, 255))
        bground.paste(png_file, (0, 0), png_file)
        bground.save(jpg_file, quality=95)
        return jpg_file

    # function ms office files to pdf
    def ms_to_pdf(self, file_name):
        command1 = 'doc2pdf ' + file_name
        subprocess.call(command1, shell=True)
        pdf_file = file_name[:file_name.find('.')] + '.pdf'
        return pdf_file

    def file_converter(self, file_name):
        ms_office = ['docx', 'doc', 'xls', 'xlsx', 'ppt',
                     'odt', 'ods']
        pngs = ['png']
        file_type = file_name[file_name.find('.') + 1:]
        if file_type in pngs:
            converted_file = self.png_to_jpg(file_name)
        elif file_type in ms_office:
            converted_file = self.ms_to_pdf(file_name)
        else:
            converted_file = file_name
        return converted_file

    def take_print(self, file_name, color_mode):
        try:
            file_to_print = self.file_converter(file_name)
            color_model = 'RGB' if color_mode == 'Colorful' else 'Blaqack&White'
            job_id = conn.printFile(self.printer, file_to_print, 'something', {'colorModel': color_model})
            printed = False
            print(color_model)
            while not printed:
                job_dict = conn.getJobAttributes(job_id)
                current_page = job_dict['job-impressions-completed']
                job_status = job_dict['job-state']
                lcd.lcd_clear()
                lcd.lcd_display_string('   Printing...   ', 1)
                lcd.lcd_display_string('   Page : {0}   '.format(current_page), 2)
                print('Current Page --> ', current_page)
                print('job state', job_status)
                if job_status == 9:
                    time.sleep(5)
                    printed = True
                elif job_status == 5:
                    time.sleep(2)
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string(' Job On Hold', 1)
                    print("Job Hold")
            else:
                print(" while loop else")
                lcd.lcd_clear()
                lcd.lcd_display_string(' Printed ', 1)
                lcd.lcd_display_string(' Successfully ', 2)
                print("Printed Successfully")
            try:
                os.remove(str(file_to_print))
            except Exception as e:
                print(e)
                pass
            self.take_otp()
        except Exception as e:
            print(e)
            self.error_message()


if __name__ == "__main__":
    Printer().take_otp()


##import cups
##conn = cups.Connection()
##job = conn.printFile('l130', 'jpg.jpg', 'my_title', {'Color_Model': 'RGB'})
### conn.cancelAllJobs()
###
### my_job = conn.getJobAttributes(5)
### my_job.get()