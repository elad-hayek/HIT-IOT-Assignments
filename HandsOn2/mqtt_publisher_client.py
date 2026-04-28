import paho.mqtt.client as mqtt  #import the client1
import time

# broker list
brokers=["localhost", "mqtt-dashboard.com", "iot.eclipse.org","broker.hivemq.com", "test.mosquitto.org"]

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
        print("message received: ",m_decode)

client = mqtt.Client("clientId-publisher", clean_session=True) # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message    
print("Connecting to broker ",broker)
port=1883
client.connect(broker,port)     #connect to broker
pub_topic= 'house/sensor/yy03'
for j in range(20):
        for i in range(20):
             client.publish(pub_topic,"my  "+str(i)+str(j)+" message")             
             time.sleep(1)
client.disconnect() # disconnect
print("End publish_client run script")

