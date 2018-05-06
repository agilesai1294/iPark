import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)


#Base Station IP Address
Broker = "xxx.xxx.xxx.xx"

#Publish to channel name along with topic
pub_topic = "channel_name/topic_name"

#Calculcating distance using ultrasonic values
def distance():
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	StartTime = time.time()
	StopTime = time.time()

	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	TimeElapsed = StopTime-StartTime
	distance = (TimeElapsed*34300)/2
	print("Distance from Node 1 is "+str(distance))
	return distance

#Data Variables used to abate false positives
samples = [0]*10
num_samples = 0
status = 0
ag_val = 0.0

#Main Function which computes the slot status using a window of 10 and
#forwards that information to base station
while True:
	dist = distance()
	if num_samples == 10:
		num_samples = 0
		avg_val = sum(samples)/float(10)

		if(avg_val < 15):
			status = 1
		else:
			status = 0

		sensor_data = [1,status]
		publish.single(pub_topic, str(sensor_data)+pub_topic, hostname=Broker)
		print("-"*10)
	samples[num_samples] = dist
	num_samples += 1

	time.sleep(1)
