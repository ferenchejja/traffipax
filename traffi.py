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
    
    gate_distance1_2=0.13*1000000*3.6  # Kapu tavolság 13cm * 1000000 (a microsec miatt) *3.6 km/h-ban legyen a végeredmény 
    gate_distance2_3=0.13*1000000*3.6  # Kapu tavolság 13cm
    gate_distance1_3=0.26*1000000*3.6  # Kapu tavolság 26cm
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
    
    irany=0 # Ha 1 akkor az 1-2-3 kapusorrend. Ha 2, 3-2-1 kapusorrend.
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
        #Szűrés
      
        if gate_1_trg==1 and  (datetime.now()-gate_1_timestamp).seconds >1:  # Ha 1 sec-ig nem történik semmi,akkor érvénytelen mérés
            print("Reset Gate1")
            gate_1_trg=0
        if gate_2_trg==1 and  (datetime.now()-gate_2_timestamp).seconds >1:
            print("Reset Gate2")
            gate_2_trg=0
        if gate_3_trg==1 and  (datetime.now()-gate_3_timestamp).seconds >1:
            print("Reset Gate3")
            gate_3_trg=0   
            
           
        
        
            
        #Kiértékelés
        if gate_1_trg==1 and gate_2_trg==1 and gate_3_trg==1:
            gate_1_trg=0
            gate_2_trg=0
            gate_3_trg=0
            if gate_1_timestamp < gate_2_timestamp and gate_2_timestamp < gate_3_timestamp: # 1-2-3 kapu sorrend
                irany=1
                time12=(gate_2_timestamp-gate_1_timestamp).microseconds
                time23=(gate_3_timestamp-gate_2_timestamp).microseconds
                time13=(gate_3_timestamp-gate_1_timestamp).microseconds
                avgtime=(time12+time23+time13)/3 
                speed12=gate_distance1_2/((gate_2_timestamp-gate_1_timestamp).microseconds)
                speed23=gate_distance2_3/((gate_3_timestamp-gate_2_timestamp).microseconds) 
                speed13=gate_distance1_3/((gate_3_timestamp-gate_1_timestamp).microseconds)
                speed=(speed12+speed23+speed13)/3
                print("          Time12: {:06d}".format(time12)," Time23: {:06d}".format(time23)," Time13: {:06d}".format(time13)," (microseconds)")
                print("1->2->3  Speed12: {:03.3f}".format(speed12)," Speed23: {:03.3f}".format(speed23),
                      " Speed13: {:03.3f}".format(speed13)," Avg.Speed: {:03.3f}".format(speed)," km/h")
                print("Hiba:    Speed12: {:02.2f}".format(100*speed12/speed-100),"% Speed23:".format(100*speed23/speed),
                      "% Speed13: {:02.2f}".format(100*speed13/speed))
                sleep(1)
                
  
            if gate_1_timestamp > gate_2_timestamp and gate_2_timestamp > gate_3_timestamp: # 3-2-1 kapu sorrend
                irany=2
                
                
                speed12=(gate_1_timestamp-gate_2_timestamp).microseconds/gate_distance1_2
                speed23=(gate_2_timestamp-gate_3_timestamp).microseconds/gate_distance2_3
                speed13=(gate_1_timestamp-gate_3_timestamp).microseconds/gate_distance1_3
                speed=(speed12+speed23+speed13)/3
                print("3->2->1  Speed12:",speed12," Speed23:",speed23," Speed13:",speed13," Avg.Speed:",speed)
                sleep(1)
                print("*")
  
        
         
      
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








