#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------

import paho.mqtt.client as mqtt
import base64
from datetime import datetime

# MQTT Settings 
Keep_Alive_Interval = 45
#Subscribe to all Sensors at Base Topic

mqttc = mqtt.Client()

def mqttclient_main(MQTT_Broker,MQTT_Port,USERNAME,PASSW):
    # Assign event callbacks
    #mqttc.on_message = on_message
    #mqttc.on_connect = on_connect

    # Connect
    mqttc.username_pw_set(USERNAME, PASSW)
    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    # Continue the network loop
    mqttc.loop_start()

