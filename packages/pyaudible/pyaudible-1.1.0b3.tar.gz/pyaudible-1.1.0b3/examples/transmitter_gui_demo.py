#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 14:19:52 2021

@author: winter_camp
"""

import tkinter as tk
import tkinter.scrolledtext as st

import pyaudio
import wave
import sys
#import matplotlib

from scipy.fftpack import fft, fftfreq
import time

#import PyA_Transmitter as pyaudible
from pyaudible import transmitter

CHUNK = 1024 * 2
FILTERED_FREQ = 500
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

FRAMES_PER_FFT = 16 # FFT takes average across how many frames
SAMPLES_PER_FFT = CHUNK * FRAMES_PER_FFT
FREQ_STEP = float(RATE)/SAMPLES_PER_FFT

CHANNEL_NUMBER = 4
SHARED_CHANNEL = 2

FRAME_TIME = 0.2


class App(object):
    
    
    display = ''
    notification = ''
    notification_framecount = 0
    received = []
    
    speed = 2
    volume = 80
    
    is_transmitting = False

    wf = 0
    
    def callback(self,in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def activate(self):
        
        if self.is_transmitting==False:
            self.p = pyaudio.PyAudio()
            self.btn_activate.config(text="Stop",fg='red')
            
            self.tx = transmitter.Transmitter(speed = self.get_speed(), volume = self.volume/100)
            self.tx.modulate_to_file(self.text_area.get('1.0', tk.END)[0:-1],'t.wav')
    
            self.wf = wave.open('t.wav', 'rb')
            print(self.wf)
            print(self.slider.get())
            
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True,
                    stream_callback=self.callback)
            
            self.stream.start_stream()
            
            self.is_transmitting = True
        else:
            self.close_audio()
        print('activate')
        return 0
    
    def close_audio(self):
        self.btn_activate.config(text="Transmit",fg='black')
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()
        self.p.terminate()
        self.is_transmitting = False
    
    def get_speed(self):
        if self.speed == 0:
            return 'slow'
        elif self.speed == 1:
            return 'medium'
        elif self.speed == 2:
            return 'fast'
        
    def speed_l(self):
        self.speed = 0
        self.refresh_speed_btn()
        return 0
    def speed_m(self):
        self.speed = 1
        self.refresh_speed_btn()
        return 0
    def speed_f(self):
        self.speed = 2
        self.refresh_speed_btn()
    
    def refresh_speed_btn(self):
        if self.speed == 0:
            self.btn_l_speed.configure(state='active')
            self.btn_m_speed.configure(state='normal')
            self.btn_f_speed.configure(state='normal')
        elif self.speed == 1:
            self.btn_l_speed.configure(state='normal')
            self.btn_m_speed.configure(state='active')
            self.btn_f_speed.configure(state='normal')
        elif self.speed == 2:
            self.btn_l_speed.configure(state='normal')
            self.btn_m_speed.configure(state='normal')
            self.btn_f_speed.configure(state='active')
    
    def __init__(self):
        self.status=-1
        self.root = tk.Tk()
        self.root.wm_title("Transmitter GUI Demo")
        
        self.text_area = st.ScrolledText(self.root,
                                         width = 38,
                                         height = 5)
        self.text_area.grid(row=0,column=0,columnspan=3)
        
        self.lbl_speed = tk.Label(master=self.root, text="Transmission Speed")
        self.lbl_speed.grid(row=3,column=0,columnspan=3)
        self.btn_l_speed = tk.Button(master=self.root, text="Slow", command=self.speed_l)
        self.btn_l_speed.grid(row=4,column=0,sticky = tk.E)
          
        self.btn_m_speed = tk.Button(master=self.root, text="Medium", command=self.speed_m)
        self.btn_m_speed.grid(row=4,column=1)  
        
        self.btn_f_speed = tk.Button(master=self.root, text="Fast", command=self.speed_f)
        self.btn_f_speed.grid(row=4,column=2,sticky = tk.W)                   
                             
        self.lbl_vol = tk.Label(master=self.root, text="Transmission Volume")
        self.lbl_vol.grid(row=5,column=0,columnspan=3)
        self.slider = tk.Scale(master=self.root, from_=0, to=100,length=200,resolution=10,showvalue=0,orient=tk.HORIZONTAL)
        self.slider.grid(row=6,column=0,columnspan=3)
        self.slider.set(80)
        #self.text_area.configure(state ='disabled')
        self.lbl_status = tk.Label(master=self.root, text="Click the button to start receiver")
        self.lbl_status.grid(row=7,column=0,columnspan=3)
        self.btn_activate = tk.Button(master=self.root, text="Transmit", command=self.activate)
        self.btn_activate.grid(row=8,column=0,columnspan=3)
        
        
        self.refresh_speed_btn()
    
    def refresh_audio_state(self):
        if self.is_transmitting and not self.stream.is_active():
            self.close_audio()


frame_count = 0
frame_num = 0
start_time = time.time()
frame_start_time = time.time()


frame_time = time.time()

app = App()

while (True):
#while (time.time()-start_time < 60):

    data = ''
    if app.status !=-1:
        while (time.time()-frame_time >= 0.1):       
            frame_time = time.time()

        frame_count += 1
        
    app.root.update_idletasks()
    app.root.update()
    app.refresh_audio_state()
    

print(frame_count/60)

