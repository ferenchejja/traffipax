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
    GPIOGATE_1=5
    GPIOGATE_2=6
    GPIOGATE_3=13
    GPIO.setup(GPIOGATE_1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GATE1
    GPIO.setup(GPIOGATE_2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GATE2
    GPIO.setup(GPIOGATE_3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GATE3
    
    gate_distance1_2=0.13 
    gate_distance2_3=0.13 # Kapu tavolság 13cm
    gate_distance1_3=0.26 # Kapu tavolság 26cm
    speed12=0 # 1 és 2 kapu között számított sebesség
    speed23=0 # 2 és 3 kapu között számított sebesség
    speed13=0 # 1 és 3 kapu között számított sebesség
    speed=0 # Számolt átlagsebesség
    
    gate_1_timestamp=datetime.now()
    gate_2_timestamp=datetime.now()
    gate_3_timestamp=datetime.now()
    gate_1_trg=0
    gate_2_trg=0
    gate_3_trg=0
    
   
     
    while True:
        
        if (not GPIO.input(GPIOGATE_1) and gate_1_trg==0):
            gate_1_trg=1
            gate_1_timestamp=datetime.now()
            print("gate1:",gate_1_timestamp)
            
        if (not GPIO.input(GPIOGATE_2) and gate_2_trg==0):
            gate_2_trg=1
            gate_2_timestamp=datetime.now()
            print("gate2:",gate_2_timestamp)
        if (not GPIO.input(GPIOGATE_3) and gate_3_trg==0):
            gate_3_trg=1
            gate_3_timestamp=datetime.now()
            print("gate3:",gate_3_timestamp)
           
        if gate_1_trg==1 and gate_2_trg==1 and gate_3_trg==1:
            #Kiértekelés
            gate_1_trg=gate_2_trg=gate_3_trg=0
            print("Megvan a három adat!")       
            sleep(0.01)       
    return
#-------------------------------------------------------------------------
def interruptmodszer():
    return
#-------------------------------------------------------------------------


GPIO.setmode(GPIO.BCM)
print("Traffipax beadandó feladat v1.0")
#hibaszamitas()
print(" Válasszon mérési módszert: 1 - poll 2 - interrupt ")
#ans=str(input())
ans="1"

if ans=="1":
    pollmodszer()
elif ans=="2":
    interruptmodszer()
else:
    print("Come on dude! Dont do it!")
    
print("DONE!")







