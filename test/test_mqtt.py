#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
aws_endpoint = "a2fmz2m3b6n0fb.iot.us-east-1.amazonaws.com"
port = 1883

def on_log(client, userdata, level, buf):
	print(buf)

def on_connect(client, userdata, flags, rc):
	if (rc == 0):
		client.connected_flag = True
		print("Connected OK")
	else:
		print("Bad connection, Returned code:", rc)
		client.loop_stop()

def on_disconnect(client, userdata, rc):
	print("Client disconnected OK")

def on_publish(client, userdata, mid):
	print("In on_pub callback mid =", mid)

mqtt.Client.connected_flag = False
client = mqtt.Client("python1")
client.on_log = on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.connect(aws_endpoint, port)
client.loop_start()

while not client.connected_flag:
	print("In wait loop")
	time.sleep(1)

time.sleep(3)
print("Publishing")

ret = client.publish("house/bulb1", "Hello World QoS-0", 0)
print("Published return =", ret)
time.sleep(3)

ret = client.publish("house/bulb1", "Hello World QoS-1", 1)
print("Published return =", ret)
time.sleep(3)

ret = client.publish("house/bulb1", "Hello World QoS-2", 2)
print("Published return =", ret)
time.sleep(3)

client.disconnect()
