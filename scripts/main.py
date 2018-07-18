#!/usr/bin/python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from os.path import abspath
import logging
import socket
import time
import json

reportInterval = 60 * 15  # 15mins [Seconds]

socketHost = '127.0.0.1'
socketPort = 17560

# Initialize the socket connection to the Df1 daemon
df1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
df1.connect((socketHost, socketPort))

mqttHost = "a2fmz2m3b6n0fb.iot.us-east-1.amazonaws.com"
mqttPort = 8883
mqttRootCAPath = abspath("certificates/RootCA.pem")
mqttCertificatePath = abspath("certificates/039b18adcd-certificate.pem.crt")
mqttPrivateKeyPath = abspath("certificates/039b18adcd-private.pem.key")
mqttTopic = "device/update_history"
mqttClientId = "50016-TEST"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(mqttClientId)
myAWSIoTMQTTClient.configureEndpoint(mqttHost, mqttPort)
myAWSIoTMQTTClient.configureCredentials(mqttRootCAPath, mqttPrivateKeyPath, mqttCertificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)    # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)            # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)       # 5 sec

# # Custom MQTT message callback
# def customCallback(client, userdata, message):
#     print("Received a new message: ")
#     print(message.payload)
#     print("from topic: ")
#     print(message.topic)
#     print("--------------\n\n")

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

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

while True:
    df1.sendall('N7:50'.encode())
    c1Power = int(s.recv(1024))
    time.sleep(1);

    df1.sendall('N7:4'.encode())
    c1Temp = int(s.recv(1024))
    time.sleep(1);

    df1.sendall('N7:49'.encode())
    c2Power = int(s.recv(1024))
    time.sleep(1);

    df1.sendall('N7:4'.encode())
    c2Temp = int(s.recv(1024))
    time.sleep(1);

    message = {}
    message['SerialNumber'] = mqttClientId
    message['Time'] = unixTime()
    message['Status'] = {
        'Cavity 1': {
            'Power': c1Power,
            'Temp': c1Temp
        },
        'Cavity 2': {
            'Power': c2Power,
            'Temp': c2Temp
        }
    }
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(mqttTopic, messageJson, 1)

    print('Published topic %s: %s\n' % (mqttTopic, messageJson))

    time.sleep(reportInterval)

s.close()
