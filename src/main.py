import paho.mqtt.client as mqtt
import base64
from Tkinter import*
import mqttclient
import settings
import tkFileDialog
import json
from datetime import datetime


def Quit(ev):
    global root
    root.destroy()
    
def connect_btn(ev):
    global data    
    if settings.os.path.isfile('config.ini'):
        try:
            data = json.load(open('config.ini'))
            mqttclient.mqttc.on_message = on_message
            mqttclient.mqttc.on_connect = on_connect
            mqttclient.mqttc.on_subscribe = on_subscribe
            mqttclient.mqttclient_main(data['IP'],data['PORT'],data['USERNAME'],data['PASSW'])
        except ValueError:
            statuslay['text'] = "not connected, check config or connection"
            statuslay.update()
    else:
        statuslay['text'] = "config file not found"
        statuslay.update()
    
def settings_btn(ev):
    settings.settings_main()
    
def download_msg_handler(data):
    if len(data)==8:
        day=data[0]
        month=data[1]
        year=data[2]
        hour=data[3]
        minute=data[4]
        seconds=data[5]
        mdata=(data[6]<<8)|data[7]
        return "%02d/%02d/%02d %02d:%02d:%02d value: %05d"%(day,month,year,hour,minute,seconds,mdata)
    else:
        return ""
    
def on_message(mosq, obj, msg):
    numdata = []
    if(data['BASE64FL'] == 'ENABLE'):
        str = "%r"%base64.b64decode(msg.payload)
    elif (data['BASE64FL'] == 'DISABLE'):
        str = msg.payload
    
    for i in str:
        numdata.append(ord(i))
    str = download_msg_handler(numdata)
    mqttdatalay['text'] = str
    mqtttopiclay['text'] = msg.topic
    datetimelay['text'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S.%f")
    datetimelay.update()
    mqttdatalay.update()
    
def on_connect(mosq, obj, flags, rc):
    data = json.load(open('config.ini'))
    mqttclient.mqttc.subscribe(data['SUBSCRIBE_TOPIC'], 0)
    statuslay['text'] = "connected"
    statuslay.update()
    print flags
    
def on_subscribe(mosq, obj, mid, granted_qos):
    statuslay['text'] = "connected and subscribed"
    statuslay.update()
    pass

def on_disconnect(mosq, obj, flags, rc):
    statuslay['text'] = "disconnected"
    statuslay.update()
    pass
def publish_btn(ev):
    global data
    global pdata
    global pdatacounter
    if(data == {}):
        publisheddata['text'] = "Published data: %s"%"not connected"
        publisheddata.update()
    else:
        if(data['PUBLISH_TOPIC'] == ''):
            publisheddata['text'] = "Published data: %s"%"not configed"
            publisheddata.update()
        else:
            if(publishdata.get() == ''):
                publisheddata['text'] = "Published data: %s"%"insert data!"
                publisheddata.update()
            else:
                try:
                    int(publishdata.get(),16)                               
                    if(pdata == publishdata.get().decode('hex')):
                        pdatacounter += 1
                        pdata = publishdata.get().decode('hex')
                        if(data['BASE64FL'] == 'ENABLE'):
                            publisheddata['text'] = "Published data: %d, %s"%(pdatacounter,base64.b64encode(pdata))
                            publisheddata.update()
                            mqttclient.mqttc.publish(data['PUBLISH_TOPIC'], base64.b64encode(pdata))
                        elif (data['BASE64FL'] == 'DISABLE'):
                            publisheddata['text'] = "Published data: %d, %r"%(pdatacounter,pdata)
                            publisheddata.update()
                            mqttclient.mqttc.publish(data['PUBLISH_TOPIC'], pdata)
                    else:
                        pdatacounter = 1
                        pdata = publishdata.get().decode('hex')
                        if(data['BASE64FL'] == 'ENABLE'):
                            publisheddata['text'] = "Published data: %d, %s"%(pdatacounter,base64.b64encode(pdata))
                            publisheddata.update()
                            mqttclient.mqttc.publish(data['PUBLISH_TOPIC'], base64.b64encode(pdata))
                        elif (data['BASE64FL'] == 'DISABLE'):
                            publisheddata['text'] = "Published data: %d, %r"%(pdatacounter,pdata)
                            publisheddata.update()
                            mqttclient.mqttc.publish(data['PUBLISH_TOPIC'], pdata)
               
                except ValueError:
                    publisheddata['text'] = "Published data: %s"%"insert data in hex"
                    publisheddata.update()
                    
                
                #publisheddata['text'] = "Published data: %s"%publishdata.get()
                #publisheddata.update()
                
    #mqttclient.mqttc.publish(data['PUBLISH_TOPIC'],publishdata.get())
    

root = Tk()
data = {}
pdata = IntVar()
pdatacounter = 0

panelFrame = Frame(root, height = 80,width = 340, bg = '#0B0354')
dataFrame = Frame(root, height = 340, bg = '#2D266A')

panelFrame.pack(side = 'top', fill = 'x')
dataFrame.pack(side = 'bottom', fill = 'both', expand = 1)

mqttdatalay = Label(dataFrame, text="", bg = '#0B0354', fg = '#E5DED4')
mqtttopiclay = Label(dataFrame, text = "", bg = '#0B0354', fg = '#E5DED4')
mqtttopichead = Label(dataFrame, text = "Data from:", bg = '#0B0354', fg = '#E5DED4')
mqttdatahead = Label(dataFrame, text = "Data value:", bg = '#0B0354', fg = '#E5DED4')
statuslay = Label(panelFrame, text="", bg = '#2D266A', fg = '#E5DED4')
publishlay = Label(dataFrame, text = "Publish data:", bg = '#0B0354', fg = '#E5DED4')
publisheddata = Label(dataFrame, text = "Published data: ", bg = '#0B0354', fg = '#E5DED4',anchor = "w")
publishdata = Entry(dataFrame,width=20,bd=3)
publishdatabtn = Button(dataFrame, text = 'Publish')


datetimelay = Label(dataFrame, text="", bg = '#0B0354', fg = '#E5DED4')
datetimeheadlay = Label(dataFrame, text="Time:", bg = '#0B0354', fg = '#E5DED4')


ConnectBtn = Button(panelFrame, text = 'Connect')
SettingsBtn = Button(panelFrame, text = 'Settings')
quitBtn = Button(panelFrame, text = 'Quit')

ConnectBtn.bind("<Button-1>", connect_btn)
SettingsBtn.bind("<Button-1>", settings_btn)
quitBtn.bind("<Button-1>", Quit)
publishdatabtn.bind("<Button-1>", publish_btn)

ConnectBtn.place(x = 10, y = 10, width = 60, height = 30)
SettingsBtn.place(x = 80, y = 10, width = 60, height = 30)
quitBtn.place(x = 150, y = 10, width = 60, height = 30)
statuslay.place(x = 10, y = 45, width = 250, height = 30)

datetimelay.place(x = 80, y = 10, width = 250, height = 30)
datetimeheadlay.place(x = 10,y = 10, width = 70, height = 30)
mqtttopichead.place(x = 10,y = 40, width = 70, height = 30)
mqtttopiclay.place(x = 80,y = 40, width = 250, height = 30)
mqttdatahead.place(x = 10, y = 70, width = 70, height = 30)
mqttdatalay.place(x = 80, y = 70, width = 250, height = 30)

publishlay.place(x = 10, y = 120, width = 70, height = 30)
publishdata.place(x = 80, y = 120, width = 250, height = 30)
publishdatabtn.place(x = 10, y = 150, width = 70, height = 30)
publisheddata.place(x = 80, y = 150, width = 250, height = 30)


root.mainloop()