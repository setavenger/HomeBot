
# import serial
import RPi.GPIO as GPIO
import time

# ser = serial.Serial("/dev/ttyACM0", 9600)  # change ACM number as found from ls /dev/tty/ACM*
# ser.baudrate = 9600


def setup_blink_board(pin):
    GPIO.setmode(GPIO.BOARD)  # choose the pin numbering
    GPIO.setup(pin, GPIO.OUT)


def blink(pin):
    setup_blink_board(11)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(20)
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    # call function on pin 11
    blink(11)
