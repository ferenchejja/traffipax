#traffipax program
#import time
#import datetime
from time import sleep
from datetime import datetime,timedelta
import RPi.GPIO as GPIO

#--------------------------------------------------------------------------------
# Kiszámítja, hogy a rpi (lassú) sebességéből adódóan mekkora mérési hiba várható
def hibaszamitas():

    elteres1=timedelta()
    totaltime=timedelta()
    for i in range(0,10):
        nw1=datetime.now()
        sleep(0.1)
        nw2=datetime.now()
        elteres1=nw2-nw1
        totaltime+=elteres1
        print("Total time:",totaltime)
        
    avgtime=totaltime-timedelta(seconds=1)
    print("Átlagos eltérés:",avgtime)
    avgmeaserror=100*avgtime/timedelta(seconds=1)
    print("Átlagos mérési hiba:",avgmeaserror," % (1% mérési hiba alatt elfogadható!)")
    print("")
    return

#-------------------------------------------------------------------------
def pollmodszer():
    print("Poll módszer")
    GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
       
    while True:
        if (GPIO.input(27)):
            print("#",end=" ")
        
        #sleep(0.0001)   
        
    return
#-------------------------------------------------------------------------
def interruptmodszer():
    return
#-------------------------------------------------------------------------


GPIO.setmode(GPIO.BCM)
print("Traffipax beadandó feladat v1.0")
#hibaszamitas()
print(" Válasszon mérési módszert: 1 - poll 2 - interrupt ")
ans=str(input())

if ans=="1":
    pollmodszer()
elif ans=="2":
    interruptmodszer()
else:
    print("Come on dude! Dont do it!")
    
print("DONE!")







