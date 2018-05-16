from Tkinter import*
import tkFileDialog
import json
import os

def save_event(objectc,variable):
    settingsvals = {}
    settingsvals['IP'] = variable['IP'].get()
    settingsvals['PORT'] = variable['PORT'].get()
    settingsvals['SUBSCRIBE_TOPIC'] = variable['SUBSCRIBE_TOPIC'].get()
    settingsvals['PUBLISH_TOPIC'] = variable['PUBLISH_TOPIC'].get()
    settingsvals['USERNAME'] = variable['USERNAME'].get()
    settingsvals['PASSW'] = variable['PASSW'].get()
    
    if(variable['base64flinvar'].get()==1):
        settingsvals['BASE64FL'] = 'ENABLE'
    elif(variable['base64flinvar'].get()==0):
        settingsvals['BASE64FL'] = 'DISABLE'
        
    with open('config.ini', 'w') as outfile:
        json.dump(settingsvals, outfile)

def Quit(objectc):
    objectc.destroy()
    
def settings_main():
    out = []
    settingsargs = {}
    settingsargs['base64flinvar'] = IntVar()
    settings = Toplevel()

    panelFrame = Frame(settings, height = 60, bg = 'gray')
    settingsFrame = Frame(settings, height = 340, width = 420)
    panelFrame.pack(side = 'top', fill = 'x')
    settingsFrame.pack(side = 'bottom', fill = 'both', expand = 1)

    iplayout = Label(settingsFrame, text = "IP address: ", anchor = "e")
    portlayout = Label(settingsFrame, text = "port: ", anchor = "e")
    sublayout = Label(settingsFrame, text = "subscribe topic: ", anchor = "e", bg = '#0B0354', fg = '#E5DED4')
    publayout = Label(settingsFrame, text = "publish topic: ", anchor = "e")
    usrlayout = Label(settingsFrame, text = "username: ", anchor = "e")
    pswlayout = Label(settingsFrame, text = "password: ", anchor = "e")
    base64sel = Label(settingsFrame, text = "base64: ", anchor = "e")
    
    settingsargs['IP'] = Entry(settingsFrame,width=20,bd=3)
    settingsargs['PORT'] = Entry(settingsFrame,width=20,bd=3)
    settingsargs['SUBSCRIBE_TOPIC'] = Entry(settingsFrame,width=20,bd=3)
    settingsargs['PUBLISH_TOPIC'] = Entry(settingsFrame,width=20,bd=3)
    settingsargs['USERNAME'] = Entry(settingsFrame,width=20,bd=3)
    settingsargs['PASSW'] = Entry(settingsFrame,width=20,bd=3)
    settingsargs['BASE64FL'] = Checkbutton(settingsFrame,text="",variable=settingsargs['base64flinvar'],onvalue=1,offvalue=0)
    
   
    if os.path.isfile('config.ini'):
        data = json.load(open('config.ini'))
        settingsargs['IP'].insert(0,data['IP'])
        settingsargs['PORT'].insert(0,data['PORT'])
        settingsargs['SUBSCRIBE_TOPIC'].insert(0,data['SUBSCRIBE_TOPIC'])
        settingsargs['PUBLISH_TOPIC'].insert(0,data['PUBLISH_TOPIC'])
        settingsargs['USERNAME'].insert(0,data['USERNAME'])
        settingsargs['PASSW'].insert(0,data['PASSW'])
        if(data['BASE64FL']=='ENABLE'):
            settingsargs['BASE64FL'].select()
        elif(data['BASE64FL']=='DISABLE'):
            settingsargs['BASE64FL'].deselect()
        
    
    
    iplayout.place(x = 10, y = 10, width = 100, height = 30)
    portlayout.place(x = 10, y = 40, width = 100, height = 30)
    sublayout.place(x = 10, y = 80, width = 100, height = 30)
    publayout.place(x = 10, y = 110, width = 100, height = 30)
    usrlayout.place(x = 10, y = 150, width = 100, height = 30)
    pswlayout.place(x = 10, y = 180, width = 100, height = 30)
    base64sel.place(x = 10, y = 220, width = 100, height = 30)
    
    
    
    settingsargs['IP'].place(x = 110, y = 10, width = 250, height = 30)
    settingsargs['PORT'].place(x = 110, y = 40, width = 250, height = 30)
    settingsargs['SUBSCRIBE_TOPIC'].place(x = 110, y = 80, width = 250, height = 30)
    settingsargs['PUBLISH_TOPIC'].place(x = 110, y = 110, width = 250, height = 30)
    settingsargs['USERNAME'].place(x = 110, y = 150, width = 250, height = 30)
    settingsargs['PASSW'].place(x = 110, y = 180, width = 250, height = 30)
    settingsargs['BASE64FL'].place(x = 110, y = 220, width = 30, height = 30)
    
    
    SavetBtn = Button(panelFrame, text = 'Save Settings')
    quitBtn = Button(panelFrame, text = 'Quit')
    SavetBtn.bind("<Button-1>",lambda e: out.append(save_event(settings,settingsargs)))
    quitBtn.bind("<Button-1>", lambda e: out.append(Quit(settings)))
    SavetBtn.place(x = 10, y = 10, width = 80, height = 30)
    quitBtn.place(x = 100, y = 10, width = 60, height = 30)
    settings.mainloop()
