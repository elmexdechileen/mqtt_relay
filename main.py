import lanrelay as ar
import paho.mqtt.client as mqtt
import os

###
# SPECIFY IN ENV:
# RELAY_IP: 10.0.0.21
# RELAY_PORT: 1234
# BASE_TOPIC: relayA
# BROKER_ADDRESS: mosquitto
# BROKER_PORT: 1883
###

rl = ar.EightChanRelay(os.environ.get('RELAY_IP'), 1234, 8)
mqttc = mqtt.Client()
topic = os.environ.get('BASE_TOPIC')
broker_address = os.environ.get('BROKER_ADDRESS')

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic + "/set/#")

def on_message(client, userdata, msg):
    try:
        index = msg.topic.split('/')[2]
        if msg.payload == "ON":
            rl.relays[index].turnOn()
        elif msg.payload == "OFF":
            rl.relays[index].turnOff()

        state = rl.relays[index].getStatus()
        mqttc.publish(topic + "/state/" + index, payload=state, qos=0, retain=True)

    except:
        mqttc.publish(topic + "/error", payload="An error occured", qos=0, retain=False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)
client.loop_forever()
