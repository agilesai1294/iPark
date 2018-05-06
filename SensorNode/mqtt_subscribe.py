from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import argparse
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

Broker = "128.237.253.81"

sub_topic = "sensor/data4"
pub_topic = "sensor/instructions"

#AWS IoT Certificat Based connection
myMQTTClient = AWSIoTMQTTClient("xxxxxxxxxxx")
myMQTTClient.configureEndpoint("xxxxxxxxxxx.iot.us-east-1.amazonaws.com",8883)
myMQTTClient.configureCredentials("/home/pi/root-CA.crt","/home/pi/ParkingCentral.private.key","/home/pi/ParkingCentral.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)

def on_connect(client,userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("test_channel")


def on_message(client,userdata,msg):
	message = str(msg.payload)
	sensor_data = message.split(',')
	id = int(sensor_data[0][1])
	status = int(sensor_data[1][1])
	messageObject = {"ID":id,"parking_status":status}
	message = json.dumps(messageObject)
	print(message)
	myMQTTClient.publish("thing01/data",message,0)
	publish.single("WSN",str(message),hostname=Broker)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker,1883,60)
client.loop_forever()
