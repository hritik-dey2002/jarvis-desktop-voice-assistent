"""
        JARVIS THE DESKTOP ASSITANT
    Jarvis is a desktop assistant. It helps the user to actively interact with the system through voice command while doing some task.
    To give any command to jarvis , the user have to say "hey Jarvis" first. Then jravis activates and says 'listenning Sir/Madam'
    To turn off jarvis, user have to say 'turn off jarvis'
    That much easy it is.
"""
# Jarvis The Desktop Assistant

########################################################################################
########################################################################################
########################################################################################

########################  Some Useful Constants ###################
setting_file_path="setting.json" # setting file
config_file_path = "config.json" # gui configuration file
RESPECTED = None

########################  Module required ###################

#  _________________________ JARVIS Audio Recognizing logic _______________________

########################  Module required ###################
from vosk import Model, KaldiRecognizer
import pyaudio
import speech_recognition as sr
import os
import threading
import json
import time
import urllib
import winshell

# getting configuration from file 'config.json'
try:
    with open(config_file_path,"r") as f:
        configx = json.load(f)
        try:
            win_config = configx["window"]
            clr_config = configx["colors"]
            pic_config = configx["picture"]
            modelFile = configx["lang_model"]  # loading the speech model
        except:
            print("configuration file is corrupted")
            time.sleep(5)
            exit(1)
        desktop=winshell.desktop()
        screenshot_fldr=desktop.replace("\\Desktop","\\Pictures\\Jarvis DA\\screenshots")
except:
    print("configuration file is missing!")
    time.sleep(5)
    exit(1)
try:
    os.makedirs(screenshot_fldr)
except:
    pass
########################  Internal logic ###################
def createRecognizer():
    """ Load the language model for recognizing the audio received from source """
    global recognizer
    recognizer = KaldiRecognizer(Model(modelFile),44100) 
    os.system('cls')
    
threading.Thread(target=createRecognizer).start()
mic = pyaudio.PyAudio() # for audio channel
os.system('cls') # clear the console

def network_status():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

def takeCommand():
    """
    Convert the user audio speech into text form and return the text
    """
    global send_btn_state
    send_btn_state=0
    window.after_cancel(showaudioWaveform)
    mic_label.configure(image=mic_img)
    if network_status():
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.pause_threshold = .8
                print("Listening...")
                audioWaveform_animation(0)
                audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
                inp_msg_label.configure(text=query,fg=random_colour_generator())
                print(f"User said : {query}")
            except Exception as e:
                query = ""
            return query
        except Exception as e:
            audioWaveform_animation(0)
            return "no_microphone"
    else:
        try:
            stream = mic.open(format=pyaudio.paInt16,channels=1,rate=96000,input=True,frames_per_buffer=1024)
            stream.start_stream()
            print("Listening...")
            audioWaveform_animation(0)
            while True:
                audio = stream.read(4096)
                query = ""
                if recognizer.AcceptWaveform(audio):
                    query = recognizer.Result()[14:-3]
                    if query != "":
                        inp_msg_label.configure(text=query,fg=random_colour_generator())
                        print(f"User said : {query}")
                        stream.close()
                        break
            return query
        except:
            audioWaveform_animation(0)
            return "no_microphone"

###XXXXXXXXXXXXXXXXXXXX   Speech to text portion completed   XXXXXXXXXXXXXXXXXXXX###
# -------------------------------------------------------------------------------- #

########################################################################################
########################################################################################
########################################################################################

import random
import psutil

########################  Useful Function ###################
def random_colour_generator(): # Random color generator
    red = format(random.randrange(0,256),'0x')
    green = format(random.randrange(0,256),'0x')
    blue = format(random.randrange(0,256),'0x')
    red = red if len(red) == 2 else f'0{red}'
    green = green if len(green) == 2 else f'0{green}'
    blue = blue if len(blue) == 2 else f'0{blue}'
    colour_generated=f"#{red}{green}{blue}"
    return colour_generated

def battery_info(): # Battery and charging status for laptop and for pc all full
    try:
        Battery = psutil.sensors_battery()
        percentage = Battery.percent
        plugged = Battery.power_plugged
    except:
        percentage = 100
        plugged = True
    return percentage,plugged

###XXXXXXXXXXXXXXXXXXXX   Some Useful Constant and Function completed   XXXXXXXXXXXXXXXXXXXX###
# ------------------------------------------------------------------------------------------- #

########################################################################################
########################################################################################
########################################################################################

#  _________________________ Gui logic _______________________

########################  Module required ###################
import tkinter
from tkinter import *
from PIL import Image , ImageTk
from datetime import datetime as dt
import tkinter.filedialog as fdilg

########################  Logic ###################

# Creating main window using Tk()
window = Tk()
# window.attributes("-fullscreen",True)
screen_width = window.winfo_screenwidth()-50
screen_height = window.winfo_screenheight()-100
# Window configuration
if win_config['width'] != -1 and win_config['height'] != -1:
    screen_width=win_config['width']
    screen_height=win_config['height']
elif win_config['width'] == -1 and win_config['height'] != -1:
    screen_height=win_config['height']
elif win_config['width'] != -1 and win_config['height'] == -1:
    screen_width=win_config['width']
window.geometry(f"{screen_width}x{screen_height}+10+10")
window.minsize(win_config["min_width"],win_config["min_height"])
window.maxsize(win_config["max_width"],win_config["max_height"])
window.title(win_config['title'])
window.iconbitmap(pic_config['icon_file'])
window.configure(background=clr_config['body'])

# Frames
Loading_Frame = Frame(master=window)
Loading_Frame.pack()
Jarvis_Frame = Frame(master=window)
Jarvis_Frame.pack(fill="both",expand=1)

## Loading_Frame configurations
# Label(master=Loading_Frame,text="loading...",font="aerial 20").pack(side="top",anchor=CENTER)
# Progressbar
# loading = Progressbar(master=Loading_Frame,maximum=100,mode="determinate",length=500,value=10)
# loading.pack()

## Jarvis_Frame configurations
# Sub frames
Main_Frame=Frame(master=Jarvis_Frame,height=290)
Main_Frame.pack(fill="both",expand=1)
Main_Frame.pack_propagate(0)
Input_Frame = Frame(master=Main_Frame,background=clr_config["body"])
Input_Frame.pack(side='left',fill="y")
Ironman_Frame = Frame(master=Main_Frame,background=clr_config["body"])
Ironman_Frame.pack(side='left',fill="both",expand=1)
Output_Frame = Frame(master=Main_Frame,background=clr_config["body"])
Output_Frame.pack(side='right',fill="y")
Bottom_Frame = Frame(master=Jarvis_Frame,background="black")
Bottom_Frame.pack(side="bottom",fill="x")

# Input_Frame
msg_inp_var = StringVar()
# Command
send_btn_state=0
def send_btn_clicked():
    global send_btn_state
    global main_logic_id
    if send_btn_state == 0:
        audio = msg_inp_var.get()
        msg_inp_var.set("")
        inp_msg_label.configure(text=audio,fg=random_colour_generator())
        send_btn_state=1
        main_logic_id = threading.Thread(target=jarvis_logic_execution,args=(audio,),daemon=True).start()
    elif send_btn_state == 1:
        audioWaveform_animation(0)
        send_btn_state=0
def send_btn_hover_state(e):
    if send_btn.cget('state')=='normal':
        send_btn.configure(bg="#ffffff",fg="#00ff3c")
def send_btn_normal_state(e):
    send_btn.configure(fg="#e0ffe9",bg="#1f0678")
mic_file = Image.open(pic_config["mic"])
mic_img = ImageTk.PhotoImage(image=mic_file)
mic_label=Label(master=Input_Frame,image=mic_img,background=clr_config["body"],width=365)
mic_label.pack(pady=20,anchor="s")
send_btn=Button(master=Input_Frame,text="Send",font=["areial",14],command=send_btn_clicked,fg="#e0ffe9",bg="#1f0678")
send_btn.pack(side="bottom")
send_btn.bind('<Enter>',send_btn_hover_state)
send_btn.bind('<Leave>',send_btn_normal_state)
text_inp = Entry(master=Input_Frame,width=30,background="#2a2b2b",fg="#17e8cc",font=["Cooper Black",18],textvariable=msg_inp_var)
text_inp.pack(side="bottom",padx=20,pady=20)
inp_msg_label = Label(master=Input_Frame,bg=clr_config['body'],font=["Cooper Black",11],wraplength=250,justify="center")
inp_msg_label.pack(side="bottom",padx=20,pady=20)

# Reading audio waveform
audioWaveformImage=Image.open(pic_config["listening"])
audioWaveform_frames=audioWaveformImage.n_frames
audioWaveform_imageObject=[tkinter.PhotoImage(file=pic_config["listening"],format=f"gif -index {i}") for i in range(audioWaveform_frames)]

showaudioWaveform=None
def audioWaveform_animation(audioWaveform_ind):
    global showaudioWaveform
    newImage=audioWaveform_imageObject[audioWaveform_ind]
    mic_label.configure(image=newImage)
    audioWaveform_ind +=1
    if audioWaveform_ind==audioWaveform_frames:
        audioWaveform_ind=0
    showaudioWaveform = window.after(150,lambda: audioWaveform_animation(audioWaveform_ind))

# Ironman_Frame
# Reading ironman gif
ironmanImage=Image.open(pic_config["iron_man"])
ironman_frames=ironmanImage.n_frames
ironman_imageObject=[tkinter.PhotoImage(file=pic_config["iron_man"],format=f"gif -index {i}") for i in range(ironman_frames)]

showIronman=None
def ironman_animation(iron_ind):
    global showIronman
    newImage=ironman_imageObject[iron_ind]
    ironman_label.configure(image=newImage)
    iron_ind +=1
    if iron_ind==ironman_frames:
        iron_ind=0
    showIronman = window.after(80,lambda: ironman_animation(iron_ind))
ironman_label = Label(master=Ironman_Frame,bg=clr_config["body"],width=300,height=screen_height-50)
ironman_label.pack()

# Output_Frame
# Reading jarvis gif
jarvisImage=Image.open(pic_config["jarvis"])
jarvis_frames=jarvisImage.n_frames
jarvis_imageObject=[tkinter.PhotoImage(file=pic_config["jarvis"],format=f"gif -index {i}") for i in range(jarvis_frames)]

showJarvis=None
def jarvis_animation(jarvis_ind):
    global showJarvis
    newImage=jarvis_imageObject[jarvis_ind]
    jarvis_logo_label.configure(image=newImage)
    jarvis_ind +=1
    if jarvis_ind==jarvis_frames:
        jarvis_ind=0
    showJarvis = window.after(200,lambda: jarvis_animation(jarvis_ind))
    
jarvis_logo_label=Label(master=Output_Frame,background=clr_config["body"],height=300)
jarvis_logo_label.pack(pady=30,padx=10)
oup_msg_label=Label(master=Output_Frame,background=clr_config['body'],wraplength=320,justify="center",font=["Cooper Black",11])
oup_msg_label.pack(padx=20,pady=20)

# Bottom_Frame
# Time Function
def time_update():
    cur_time = dt.now().strftime("%H:%M:%S")
    # print(cur_time)
    time_label.configure(text=cur_time,foreground=random_colour_generator())
    window.after(1000,time_update)
# Date Function
def date_update():
    cur_date = dt.now().strftime("%d/%m/%Y")
    date_label.configure(text=cur_date,foreground=random_colour_generator())
    window.after(5000,date_update)
def power_info():
    power_label.configure(text=f"{battery_info()[0]}%",foreground=random_colour_generator())
    window.after(3000,power_info)
def plugged_info():
    plugged_label.configure(text=f"{'Plugged' if battery_info()[1] else 'Unplugged'}",foreground=random_colour_generator())
    window.after(3000,plugged_info)
def terminateProgram():
    speak(f"Turning OFF, {RESPECTED}!.")
    window.after_cancel(showIronman)
    window.after_cancel(showJarvis)
    Loading_Frame.destroy()
    Jarvis_Frame.destroy()
    window.destroy()
    exit()
def exit_btn_hover_state(e):
    if exit_btn.cget('state')=='normal':
        exit_btn.configure(bg="#575454",fg="#8f1755")
def exit_btn_normal_state(e):
    exit_btn.configure(bg=clr_config["body"],fg="red")
time_label=Label(master=Bottom_Frame,font=["sans serif", 27 ,"bold"],background=clr_config['body'])
time_label.pack()
date_label=Label(master=Bottom_Frame,font=["sans serif", 27 ,"bold"],background=clr_config['body'])
date_label.pack(side="left",anchor="n")
exit_btn=Button(master=Bottom_Frame,text="Exit",fg="red",bg=clr_config["body"],font=["Bodoni MT Black", 18 ,"bold"],command=terminateProgram,activeforeground="#660a0a",activebackground="#c7c5c5")
exit_btn.pack(side="right")
exit_btn.bind('<Enter>',exit_btn_hover_state)
exit_btn.bind('<Leave>',exit_btn_normal_state)
power_label = Label(master=Bottom_Frame,font=["sans serif", 20 ,"bold"],background=clr_config['body'])
power_label.pack(side="right",padx=20)
plugged_label = Label(master=Bottom_Frame,font=["sans serif", 20 ,"bold"],background=clr_config['body'])
plugged_label.pack(side="right",padx=20)

# starting the requirement function
window.after(200,ironman_animation,0)
window.after(200,jarvis_animation,0)
window.after(200,time_update)
window.after(200,date_update)
window.after(200,power_info)
window.after(200,plugged_info)

###XXXXXXXXXXXXXXXXXXX  POPUP LOGIC XXXXXXXXXXXXXXXXXXXX###
# variables
app_name = StringVar() 
app_path = StringVar() 
url_name = StringVar()
url_pattern = StringVar() 
user_field = StringVar() 
user_value = StringVar()
target=None
def get_application_path():
    global app_path
    app_path.set(fdilg.askopenfile(filetypes=[['Exe files','*.exe']]).name)
    # update_all()
    
def clear_variables():
    global target
    target = None
    app_name.set("")
    app_path.set("")
    url_name.set("")
    url_pattern.set("")
    user_field.set("")
    user_value.set("")
    popup.destroy()

def on_submit():
    with open(setting_file_path,"r") as f:
        configx = json.load(f)
    if target == "applications":
        key = app_name.get().lower()
        value = app_path.get()
    elif target == "urls":
        key = url_name.get().lower()
        value = url_pattern.get()
    elif target == "user":
        key = user_field.get().lower()
        value = user_value.get()
    configx[target][key]=value
    with open(setting_file_path,"w") as f:
        json.dump(configx,f)
    speak(f"{target} added")
    clear_variables()    

def update_all():
    global popup
    global app_name
    global app_path
    global url_name
    global url_pattern
    global user_field
    global user_value
    popup_font = ['Calibri (Body)',10]
    popup_bg = "#0b3040"
    popup_fg = "#ffffff"
    popup = Toplevel(window)
    if target == 'applications':
        popup.geometry(f"{410}x{150}+100+70")
    else:
        popup.geometry(f"{320}x{150}+100+70")
    # popup.overrideredirect(True)
    popup.configure(bg=popup_bg)
    if target == 'applications':
        Label(master=popup,text='Enter application name',font=popup_font,bg=popup_bg,fg=popup_fg).grid(row=0,column=0,padx=10,pady=10)
        app_name_entry = Entry(master=popup,textvariable=app_name,font=popup_font)
        app_name_entry.grid(row=0,column=1,padx=10,pady=10)
        Label(master=popup,text='Enter path',font=popup_font,bg=popup_bg,fg=popup_fg).grid(row=1,column=0,padx=10,pady=10)
        path_label_entry=Entry(master=popup,textvariable=app_path,font=popup_font)
        path_label_entry.grid(row=1,column=1,padx=10,pady=10)
        Button(master=popup,text="Browse",command=get_application_path,font=popup_font).grid(row=1,column=2,padx=10,pady=10)
    elif target == 'urls':
        Label(master=popup,text='Enter website name',font=popup_font,bg=popup_bg,fg=popup_fg).grid(row=0,column=0,padx=10,pady=10)
        app_name_entry = Entry(master=popup,textvariable=url_name,font=popup_font)
        app_name_entry.grid(row=0,column=1,padx=10,pady=10)
        Label(master=popup,text='Enter URL',font=popup_font,bg=popup_bg,fg=popup_fg).grid(row=1,column=0,padx=10,pady=10)
        path_label_entry=Entry(master=popup,textvariable=url_pattern,font=popup_font)
        path_label_entry.grid(row=1,column=1,padx=10,pady=10)
    elif target == 'user':
        Label(master=popup,text='Enter field name',font=popup_font,bg=popup_bg,fg=popup_fg).grid(row=0,column=0,padx=10,pady=10)
        app_name_entry = Entry(master=popup,textvariable=user_field,font=popup_font)
        app_name_entry.grid(row=0,column=1,padx=10,pady=10)
        Label(master=popup,text='Enter field value',font=popup_font,bg=popup_bg,fg=popup_fg).grid(row=1,column=0,padx=10,pady=10)
        path_label_entry=Entry(master=popup,textvariable=user_value,font=popup_font)
        path_label_entry.grid(row=1,column=1,padx=10,pady=10)
    Button(master=popup,text="Submit",command=on_submit).grid(row=2,column=1,pady=10)
    Button(master=popup,text="Cancel",fg="red",command=clear_variables).grid(row=2,column=0,pady=10)

###XXXXXXXXXXXXXXXXXXXX   GUI Logic Completed   XXXXXXXXXXXXXXXXXXXX###
# ------------------------------------------------------------------- #

########################################################################################
########################################################################################
########################################################################################

#  _________________________ JARVIS logic _______________________

########################  Module required ###################
import pyttsx3 # python text to speech is used for converting text into voice
import requests # request is used for geting response from internet 
from datetime import date, datetime
import wikipedia
import webbrowser
import difflib
import win32com.client
import pyautogui
import socket

########################  Logic ###################
shell = win32com.client.Dispatch("WScript.Shell")
list_files={}
def keyValueApp(file,realPath):
    key=file.replace(".lnk","").lower()
    if not key.isalpha():
        temp=""
        for letter in key:
            if letter in ["0","1","2","3","4","5","6","7","8","9","."]:
                pass
            elif letter == "_":
                temp+=" "
            elif letter == "+":
                temp+=" plus "
            else:
                temp+=letter
        key=temp.strip()
    return key,shell.CreateShortCut(realPath).Targetpath

def serachAllApplication(location):
    folder=os.listdir(location)
    for file in folder:
        realPath=os.path.join(location,file)
        if file.endswith(".lnk"):
            key,value=keyValueApp(file,realPath)
            list_files[key]=value
        elif "." in file:
            pass
        else:
            serachAllApplication(realPath)
            
def updateApplicationInSetting():    
    serachAllApplication("C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
    with open(setting_file_path,"r") as f:
            configx = json.load(f)
    for keys in list_files.keys():
        configx["applications"][keys]=list_files[keys]
    with open(setting_file_path,"w") as f:
        json.dump(configx,f) 
def get_configuration():
    try:
        with open(setting_file_path,"r") as f:
            configx = json.load(f)
            applications = configx['applications']
            urls = configx['urls']
            user = configx['user']
        global RESPECTED
        RESPECTED = "Sir" if user['gender'].lower()=="male" else "Madam" if user['gender'].lower() == "female" else "Master"
        return applications, urls, user
    except Exception as e:
        print(e)
        configx = {'applications':{'notepad':'notepad','calculator':'calc.exe'},'urls':{'youtube':'youtube.com'},'user':{'name':'','gender':'','place':''}}
        with open(setting_file_path,"w") as f:
            json.dump(configx,f)     
    
get_configuration()
updateApplicationInSetting()

""" __ Setting up the engine to speak using the module pyttsx3 __"""
engine=pyttsx3.init()

""" __ Setting up some properties of the speaking engine __ """
voices=engine.getProperty('voices') # get the voices available in the local machine
engine.setProperty('voice',voices[0].id) # write voices[0].id for male voice and voices[1].id for female (speaking voice)
engine.setProperty('rate',190) # write in between 100 - 300. 100 is slower and 300 is much faster (speaking speed)
""" __ Speaking engine basic setup is done __"""

def speak(audio):
    """ __ it give Jarvis the opportunity  to speak the message it receive as a paramater __ """
    oup_msg_label.configure(text=audio,fg=random_colour_generator())
    send_btn.configure(state="disabled")
    exit_btn.configure(state="disabled")
    engine.say(audio)
    engine.runAndWait()
    send_btn.configure(state="normal")
    exit_btn.configure(state="normal")
    # End of speak(audio)
    
def get_greet():
    hrs = int(datetime.now().hour)
    if hrs >= 0 and hrs < 12:
        return 'Good Morning'
    elif hrs >= 12 and hrs < 18:
        return 'Good Afternoon'
    else:
        return 'Good Evening'
def get_today():
    today = date.today().strftime("%A, %d %B %Y")
    return today

def special_greet():
    if get_greet() == "Good Morning":
        audio = f"For now feel free to grab a cup of coffee, and have a good day, {RESPECTED} !"
    elif get_greet() == "Good Afternoon":
        audio = f"Have a good day, {RESPECTED}"
    else:
        audio = ""
    return audio
def weatherReport():
    user = get_configuration()[2]
    if user['place']!="":
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={user['place']}&units=metric&appid=858f54c9786e8dab5e2306b06f55df26"
            data = requests.get(url)
            data = data.json()
            return f"""The weather in {data['name']} is {round(data['main']['temp'])} degree centigrade, and humidity {round(data['main']['humidity'])} percent"""
        except:
            return "Since you does not connected to a network. I can't tell you the weather report"
    else:
        return "Since your location is not set, I can't tell you the weather report"

def wish():
    user = get_configuration()[2]
    audio = f"""{get_greet()} {user['name']}. Today is {get_today()}. {weatherReport()}. Importing all preferences from home interface. Your systems are now fully operationl. {special_greet()}"""
    speak(audio)

def open_application(target):
    applications = get_configuration()[0]
    speak(f"opening {target}")
    os.startfile(applications[target])

def open_url(target):
    applications,urls,_ = get_configuration()
    try:
        browser=applications['browser']
    except:
        browser="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    webbrowser.register(
        'chrome', None, webbrowser.BackgroundBrowser(browser))
    speak(f"opening {target}")
    webbrowser.get('chrome').open_new_tab(urls[target])

def wikipedia_search(query):
    try:
        results = wikipedia.summary(query,sentences=2)
        audio = f"Searching wikipedia. According to wikipedia, {results}"
    except Exception as e:
        audio = f"Can not get it, {RESPECTED}"
    return audio


def jarvis_logic_execution(query):  # Main Logic Here
    global send_btn_state
    global target
    send_btn_state=0
    window.after_cancel(showaudioWaveform)
    mic_label.configure(image=mic_img)
    application_keys = get_configuration()[0].keys()
    url_keys = get_configuration()[1].keys()
    greet=difflib.get_close_matches(query,['hi jervis','hello jervis','namaste jervis'])
    uau = difflib.get_close_matches(query,['add applications','add urls','add user'])
    if 'open' in query:
        query=query.replace("open","")
        app_to_open = difflib.get_close_matches(query,application_keys)
        url_to_open = difflib.get_close_matches(query,url_keys)
        if app_to_open:
            open_application(app_to_open[0])
        elif url_to_open:
            open_url(url_to_open[0])
    elif uau:
        uau=uau[0]
        uau=uau.replace("add ","")
        target=uau
        update_all()
    elif greet:
        speak(f"{greet[0].replace('jervis','')}{RESPECTED}")
    elif 'wikipedia' in query:
        command =  query.replace("wikipedia","")
        speak(wikipedia_search(command))
    elif 'weather report' in query:
        speak(weatherReport())
    elif 'date' in query:
        speak(get_today())
    elif 'time' in query:
        speak(dt.now().strftime("%I:%M %p"))
    elif difflib.get_close_matches(query,['turn off jarvis',"turn off gervais",'turn off jervis']):
        terminateProgram()
    elif difflib.get_close_matches(query,['shutdown','shut down']):
        speak("Shutting down system after 30 second.")
        time.sleep(30)
        os.system("shutdown -s")
    elif difflib.get_close_matches(query,['restart','re start']):
        speak("Restarting system after 30 second.")
        time.sleep(30)
        os.system("shutdown -r")
    elif "read" in query:
        query=query.replace("read ","")
        speak(f"Reading, {query}")
    elif difflib.get_close_matches(query,['screenshot',"take screenshot"]):
        fileN=f"{socket.gethostname()}_{os.getlogin()}_{dt.now().strftime('%d%m%Y%H%M%S')}.png"
        speak("Taking screenshot")
        screen = pyautogui.screenshot()
        screen.save(f"{screenshot_fldr}/{fileN}")
        speak("Screenshot saved")
    audioWaveform_animation(0)
def jarvis_begin():
    wish()
    audioWaveform_animation(0)
    while 1:
        while 1:
            query = takeCommand().lower()
            if query == "no_microphone":
                break
            elif difflib.get_close_matches(query,['hey gervais','hi jervis','hello gervais']) :
                speak(f"Listening. {RESPECTED}")
                break
            elif difflib.get_close_matches(query,["turn off gervais",'turn off jervis']) :
                terminateProgram()
        query = takeCommand().lower()
        if query == "no_microphone":
            break
        else:
            jarvis_logic_execution(query)

###XXXXXXXXXXXXXXXXXXXX   Jarvis Logic Completed   XXXXXXXXXXXXXXXXXXXX###
# ---------------------------------------------------------------------- #

# --------------------------- MAINLOOP ----------------------- #
jarvis_id=threading.Thread(target=jarvis_begin)
jarvis_id.daemon = True
window.after(20,jarvis_id.start())
window.mainloop()
#XXXXXXXXXXXXXXXXXX JARVIS IMPLEMENTATION COMPLETED XXXXXXXXXXXXXXXXXXXX#
