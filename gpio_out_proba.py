from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)


GPIO.output(21,True)
sleep(1)
GPIO.output(21,False)
   
GPIO.cleanup(21)
