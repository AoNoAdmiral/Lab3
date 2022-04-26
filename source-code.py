
import paho.mqtt.client as mqttclient
import time
import json
import geocoder
import serial.tools.list_ports
import serial

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "LyoSMl8n9Yoki1fBpJoj"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0]=="1":
        client.publish('v1/devices/me/telemetry', json.dumps({'temperature':splitData[1]}), 1)
    if splitData[0]=="2":
        client.publish('v1/devices/me/telemetry', json.dumps({'light':splitData[1]}), 1)
        

def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if temp_data['value']==1:
                ser.write(("1#").encode())
            else:
                ser.write(("0#").encode())
        if jsonobj['method'] == "setPUMP":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if temp_data['value']==1:
                ser.write(("4#").encode())
            else:
                ser.write(("3#").encode())
    except:
        pass




def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

client = mqttclient.Client("GATE")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 100
counter = 0
mess = ""
ser = serial.Serial(port="COM8", baudrate=115200)
    
while True:
    # client.publish('v1/devices/me/rpc/request/1',json.dumps(request), 1)
    readSerial()
    # client.publish('v1/devices/me/telemetry', json.dumps({'temperature':50,'light':30}), 1)
    time.sleep(5)
# https://demo.thingsboard.io/dashboard/50770330-7826-11ec-91d1-9b16bfb7b504?publicId=e1aef1d0-7823-11ec-91d1-9b16bfb7b504
