# Import Python GPIO library
import RPi.GPIO as GPIO
# Import time library
import time

import socket

# Set GPIO pin numbering
GPIO.setmode(GPIO.BCM)

# Name input and output pins
TRIG=23
ECHO=24

# Print message to let the user know measurement is in progress
print ("Distance Measurement in Progress")

# Set the two GPIO ports as either inputs or outputs
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Komunikacija izmedju 2 raspberrya, UDP_IP je IP Raspb Zero W, a UDP_PORT ne znamo sto 6677 ali radi
UDP_IP = "192.168.43.237"
UDP_PORT = 6677
while True:
    #time.sleep(0.1)
    zbir = 0
    #Pocinje petlja ovdje
    for i in range (5):
        # Ensure that the Trigger pin is set low
        GPIO.output(TRIG,False)
        
        # The sensor needs a moment
        #print ("Waiting for the sensor to settle")
        time.sleep(0.1)

        # Create trigger pulse and set to high
        GPIO.output(TRIG, True)

        # For 10us
        time.sleep(0.00001)

        # Set to low again
        GPIO.output(TRIG, False)

        pulse_start=0
        pulse_end=0

        #   Record the last low timestamp for ECHO just before signal is received and the pin goes high
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        #   Record the last high timestamp for ECHO
        while GPIO.input(ECHO)==1:
            pulse_end=time.time()

        # Calculate the difference between the two recorded timestamps to get the duration of pulse and assign that value to pulse_duration
        pulse_duration=pulse_end - pulse_start

        # Calulate the distance
        distance=pulse_duration * 17150

        # Round the distance to 2 decimal places
        distance=round(distance, 2)

       # print ("Pojedinacna distanca",distance,"cm")
        zbir+=distance

    aritmeticka_sredina = round(zbir/5)
    if (aritmeticka_sredina<10):
        MESSAGE = ('00' + str(aritmeticka_sredina)).encode('utf-8')
    elif (aritmeticka_sredina<100):
        MESSAGE = ('0'+str(aritmeticka_sredina)).encode('utf-8')
    else:
        MESSAGE = str(aritmeticka_sredina).encode('utf-8')


    #MESSAGE = str(aritmeticka_sredina).encode('utf-8')

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    #print (sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)))
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    # Print the distance

   # print ("Distanca zbir:",aritmeticka_sredina,"cm")



# Clean the GPIO pins
GPIO.cleanup()