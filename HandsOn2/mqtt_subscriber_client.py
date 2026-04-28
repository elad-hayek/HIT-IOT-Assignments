import paho.mqtt.client as mqtt  #import the client1
import time

# broker list
brokers=["localhost","mqtt-dashboard.com", "iot.eclipse.org","broker.hivemq.com","test.mosquitto.org"]

broker=brokers[0]

def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
def on_message(client,userdata,msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("Now message received: ",m_decode)
        print("It was topic: ", topic)
        if "send message" in m_decode:
                client.publish(pub_topic,'returned message')


client = mqtt.Client("clientId-subscriber", clean_session=True) # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message

    
print("Connecting to broker ",broker)
port=1883
client.connect(broker,port)     #connect to broker

sub_topic= 'house/sensor/yy03'
pub_topic= 'house/sensor/yy/pub'

client.loop_start()  #Start loop
client.subscribe(sub_topic)
time.sleep(10)
client.loop_stop()    #Stop loop 
client.disconnect()