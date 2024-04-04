#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import random

import paho.mqtt.client as paho
from paho import mqtt




# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)




# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))




# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))




# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )
        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))



### CLIENT 1

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client1 = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1, client_id="Client_1", userdata=None, protocol=paho.MQTTv5)
client1.on_connect = on_connect
# enable TLS for secure connection
client1.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client1.username_pw_set("ECE_140B", "ECE_140BPasscode")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client1.connect("a7d11f6ab497494cb309b9bc9a40c69f.s1.eu.hivemq.cloud", 8883)
# setting callbacks, use separate functions like above for better visibility
client1.on_subscribe = on_subscribe
client1.on_message = on_message
client1.on_publish = on_publish


### CLIENT 2
client2 = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1, client_id="Client_2", userdata=None, protocol=paho.MQTTv5)
client2.on_connect = on_connect
# enable TLS for secure connection
client2.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client2.username_pw_set("ECE_140B", "ECE_140BPasscode")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client2.connect("a7d11f6ab497494cb309b9bc9a40c69f.s1.eu.hivemq.cloud", 8883)
# setting callbacks, use separate functions like above for better visibility
client2.on_subscribe = on_subscribe
client2.on_message = on_message
client2.on_publish = on_publish

### CLIENT 3
client3 = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1, client_id="Client_3", userdata=None, protocol=paho.MQTTv5)
client3.on_connect = on_connect
# enable TLS for secure connection
client3.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client3.username_pw_set("ECE_140B", "ECE_140BPasscode")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client3.connect("a7d11f6ab497494cb309b9bc9a40c69f.s1.eu.hivemq.cloud", 8883)
# setting callbacks, use separate functions like above for better visibility
client3.on_subscribe = on_subscribe
client3.on_message = on_message
client3.on_publish = on_publish

client3.subscribe("number/randomNums", qos=1)
client3.loop_start()

ind = 0
while True:
    num1 = random.random()
    num2 = random.random()
    client1.publish("number/randomNums", payload=num1, qos=1)
    client2.publish("number/randomNums", payload=num2, qos=1)
    time.sleep(3)
    ind+=1
    if ind>5:
        break

# # subscribe to all topics of encyclopedia by using the wildcard "#"
# client.subscribe("encyclopedia/#", qos=1)


# # a single publish, this can also be done in loops, etc.
# client.publish("encyclopedia/temperature", payload="hot", qos=1)


# # loop_forever for simplicity, here you need to stop the loop manually
# # you can also use loop_start and loop_stop
# client1.loop_forever()
# client2.loop_forever()
# client3.loop_forever()
