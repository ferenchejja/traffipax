#traffipax program
#import time
#import datetime
from time import sleep
from datetime import datetime,timedelta
import RPi.GPIO as GPIO

#--------------------------------------------------------------------------------
# Két datetime változó különbségét adja másodpercben
def idokulonbseg( time1 , time2 ):

    if time1>time2:
       timediff=(time1-time2).seconds+(time1-time2).microseconds/1000000
    else:
       timediff=(time2-time1).seconds+(time2-time1).microseconds/1000000
    return(timediff)

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
    
    gate_distance1_2=0.26*3.6  # Kapu tavolság 26cm  *3.6, hogy km/h-ban legyen a végeredmény 
    gate_distance2_3=0.13*3.6  # Kapu tavolság 13cm
    gate_distance1_3=0.39*3.6  # Kapu tavolság 26cm
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
            #print("gate1:",gate_1_timestamp)
            
        if (not GPIO.input(GPIOGATE_2) and gate_2_trg==0):
            gate_2_trg=1
            gate_2_timestamp=datetime.now()
            #print("gate2:",gate_2_timestamp)
        if (not GPIO.input(GPIOGATE_3) and gate_3_trg==0):
            gate_3_trg=1
            gate_3_timestamp=datetime.now()
            #print("gate3:",gate_3_timestamp)
        #Szűrés
      
        if gate_1_trg==1 and  idokulonbseg(datetime.now(),gate_1_timestamp) >2:  # Ha 2 sec-ig nem történik semmi,akkor érvénytelen mérés
           print("Reset Gate1")
           gate_1_trg=0
        if gate_2_trg==1 and  idokulonbseg(datetime.now(),gate_2_timestamp) >2:
           print("Reset Gate2")
           gate_2_trg=0
        if gate_3_trg==1 and  idokulonbseg(datetime.now(),gate_3_timestamp) >2:
           print("Reset Gate3")
           gate_3_trg=0   
            
      #Kiértékelés
        if gate_1_trg==1 and gate_2_trg==1 and gate_3_trg==1:
            gate_1_trg=0
            gate_2_trg=0
            gate_3_trg=0
            if gate_1_timestamp < gate_2_timestamp and gate_2_timestamp < gate_3_timestamp: # 1-2-3 kapu sorrend
               print("->1->2->3->")
               irany=1
            if gate_1_timestamp > gate_2_timestamp and gate_2_timestamp > gate_3_timestamp: # 3-2-1 kapu sorrend
               print("->3->2->1->")
               irany=2
                                
            time12=idokulonbseg(gate_2_timestamp,gate_1_timestamp)  # sec-ben
            time23=idokulonbseg(gate_2_timestamp,gate_3_timestamp)
            time13=idokulonbseg(gate_3_timestamp,gate_1_timestamp) 
            avgtime=(time12+time23+time13)/3 
            speed12=gate_distance1_2/time12 
            speed23=gate_distance2_3/time23 
            speed13=gate_distance1_3/time13 
            speed=(speed12+speed23+speed13)/3
            print("Time12: {:02.6f}".format(time12)," Time23: {:02.6f}".format(time23)," Time13: {:02.6f}".format(time13)," (sec)")
            print("Time hiba (t12+t23)/t13) {:02.6f}".format( 100*(time12+time23)/time13)," %" )
            print("Speed12: {:03.3f}".format(speed12)," Speed23: {:03.3f}".format(speed23)," Speed13: {:03.3f}".format(speed13)," Avg.Speed: {:03.3f}".format(speed)," km/h")
            print("Hiba: Speed12: {:02.2f}".format(100*speed12/speed-100),"% Speed23: {:02.2f}".format(100*speed23/speed-100),
                  "% Speed13: {:02.2f}".format(100*speed13/speed-100))
            sleep(1)
            
          
        
         
      
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








