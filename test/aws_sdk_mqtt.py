#!/usr/bin/python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from os.path import abspath
import logging
import time
import json

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

port = 8883
host = "a2fmz2m3b6n0fb.iot.us-east-1.amazonaws.com"
rootCAPath = abspath("certificates/RootCA.pem")
certificatePath = abspath("certificates/039b18adcd-certificate.pem.crt")
privateKeyPath = abspath("certificates/039b18adcd-private.pem.key")
topic = "device/update_history"
clientId = "50016-TEST"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)    # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)            # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)       # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

time.sleep(2)

def unixTime():
    return int(time.time() * 1000)

AddressDatabase = {
    'Cavity 1': {
        'Power': 'N7:50',  # HMI Display Minutes
        'Temp': 'N7:4'     # Temperature [C]
    },
    'Cavity 2': {
        'Power': 'N7:49',  # HMI Display Hours
        'Temp': 'N7:4'     # Temperature [C]
    }
}

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    message = {}
    message['SerialNumber'] = clientId
    message['Time'] = unixTime()
    message['Status'] = {
        'Cavity 1': {
            'Power': 729,
            'Temp': 32
        }
    }
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)

    print('Published topic %s: %s\n' % (topic, messageJson))

    loopCount += 1
    time.sleep(5)
