# Script will be used to read sensor data and then post the IoT Thinkspeak
# Read Temprature & Humidity using DHT11 sensor attached to raspberry PI
# Program posts these values to a thingspeak channel
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2
DEBUG = 1
# Define GPIO pin to which DHT11 is connected
DHTpin = 24  #27 datos externos
#Setup our API and delay
myAPI = "0XCBM8VUSO54A8G0"  # API Key from thingSpeak.com channel
myDelay = 60 #how many seconds between posting data
GPIO.setmode(GPIO.BCM)  

def getSensorData():
    print "Lectura de sensores:";
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHTpin)
    hum_ext, temp_ext = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 27)
    if humidity is not None and temperature is not None:
        print('Temperatura interna={0:0.1f}*C  Humedad interna={1:0.1f}%'.format(temperature, humidity))
        
    else:
        print('Fallo al leer los datos en el sensor interno. Intente de nuevo!')

    if hum_ext is not None and temp_ext is not None:
	print('Temperatura externa={0:0.1f}*C  Humedad externa={1:0.1f}%'.format(temp_ext, hum_ext))
    else:
 	print('Fallo al leer los datos en el sensor externo. Intente de nuevo!')
    return (str(humidity), str(temperature),str(hum_ext), str(temp_ext))


def main():
    print 'Iniciando conexion...'
    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    preti = 0
    prete = 0
    prehi = 0
    prehe = 0
    limite = 7
    x = 0
    while True:
        try:
            print "Leyendo valores ahora"
            hum_i, temp_i, hum_e, temp_e = getSensorData()
	    
	    if x==1:
	        tempti = float(temp_i)
		tempte = float(temp_e)
		temphi = float(hum_i)
		temphe = float(hum_e)

		dist1 = tempti - preti
		if abs(dist1) > limite:
		    temp_i = preti
    	        dist2 = tempte - prete
		if abs(dist2) > limite:
		    temp_e = prete

		dist3 = temphi - prehi
		if abs(dist3) > limite:
		    hum_i = prehi

		dist4 = temphe - prehe
		if abs(dist4) > limite:
		     hum_e = prehe

	    a = str(temp_i)
	    b = str(temp_e)
	    c = str(hum_i)
	    d = str(hum_e)
	    x = 1

            print a + " " + b+ " " + c + " " + d + " "
            f = urllib2.urlopen(baseURL + "&field1=%s&field2=%s&field3=%s&field4=%s" % (a, b, c, d))
            preti = float(a)
	    prete = float(b)
            prehi = float(c)
	    prehe = float(d)
	    print f.read()
            f.close()
            sleep(int(myDelay))
        except Exception as e:
            print e
            print 'Reintentando conectar...\n'
            sleep(int(10))

# call main

if __name__ == '__main__':
    main()

