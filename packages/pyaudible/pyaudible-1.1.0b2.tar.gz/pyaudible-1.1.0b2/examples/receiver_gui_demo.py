"""PyAudible Receiver GUI Example"""

import tkinter as tk
import tkinter.scrolledtext as st

import matplotlib.pyplot as plt
import time

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pyaudible import receiver

CHUNK = 1024 * 2
RATE = 44100
FRAME_RATE = 0.2

class GUI(object):
    
    display = ''
    notification = ''
    notification_framecount = 0
    received = []

    
    def activate(self):
        if self.status==-1:
            self.btn_activate.config(text="Stop",fg='red')
            self.status = 0
        else:
            self.btn_activate.config(text="Activate",fg='black')
            self.status = -1
            self.lbl_display['text'] = ''
            self.display = ''
            self.lbl_status['text'] = "Click the button to start receiver"
        return 0
    
    def __init__(self):
        self.status=-1
        self.root = tk.Tk()
        self.root.wm_title("Receiver GUI Demo")
        
        self.text_area = st.ScrolledText(self.root,
                                         width = 5,
                                         height = 20)
        self.text_area.pack(fill=tk.X)
        
        self.text_area.configure(state ='disabled')
        
        self.btn_activate = tk.Button(master=self.root, text="Activate", command=self.activate)
        self.btn_activate.pack(fill=tk.X)
        
        self.lbl_status = tk.Label(master=self.root, text="Click the button to start receiver")
        self.lbl_status.pack(fill=tk.X)
        self.lbl_display = tk.Label(master=self.root, text="", fg="grey")
        self.lbl_display.pack(fill=tk.X)
        
        self.fig, self.ax2 = plt.subplots(figsize=(4,1.5))
        x_fft = np.linspace(0, RATE, CHUNK)
        self.line_fft, = self.ax2.semilogx(x_fft, np.zeros(CHUNK), '-', lw = 0.5,color="black")
        self.ax2.set_xlim(20, RATE/2)
        self.ax2.set_ylim(0, 5)
        self.ax2.set_facecolor((0.925,0.925,0.925))
        self.fig.patch.set_facecolor((0.925,0.925,0.925))
        plt.axis('off')
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.fig.canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def on_activate(self):
        if self.status == -1:
            return False
        else:
            return True
        
    def update_text(self, received_list):
        self.received.append((received_list[-1],time.asctime( time.localtime(time.time()) )))
        texts = ''
        texts += self.received[-1][1] + '\n' + self.received[-1][0] + '\n\n'
            
        self.text_area.configure(state ='normal')
        self.text_area.insert(tk.INSERT,texts)
        self.text_area.configure(state ='disabled')
        return 0

    def handle_status(self, data,status):
        self.status = status
        if self.status == 0:
            self.lbl_status['text'] = 'Waiting for a transmission...'
            
        elif self.status == 1:
            self.lbl_display['text'] = ''
            self.display = ''
            self.notification_framecount = 0
            self.lbl_status['text'] = 'Connecting...'
           
        elif self.status == 3:
            self.notification = 'Connection Failed, increase volume'
            self.notification_framecount = 1
        
        elif self.status == 4:
            if data:
                self.display += data
            self.lbl_status['text'] = 'Listening...'
            self.lbl_display['text'] = self.display
            
        elif self.status == 5:
            self.notification = 'Text Received Successfully!'
            self.notification_framecount = 1
            
        elif self.status == 6:
            self.notification = 'Transmission failed, try again'
            self.notification_framecount = 1
            
        if self.notification_framecount>0 and self.notification_framecount<60:
            self.lbl_status['text'] = self.notification
            self.notification_framecount += 1
        elif self.notification_framecount >=60:
            self.notification_framecount = 0
            self.lbl_display['text'] = ''
            self.display = ''
        return 0
    
    def update_spectrum(self, fft):
        self.line_fft.set_ydata(np.abs(fft[0:CHUNK]) * 2 / (256 * CHUNK) )
        self.ax2.draw_artist(self.ax2.patch)
        self.ax2.draw_artist(self.line_fft)
        self.fig.canvas.blit()
        self.fig.canvas.flush_events()
        
        return 0
    
    def update_ui(self):
        self.root.update_idletasks()
        self.root.update()


# instantiate the GUI and the receiver
app = GUI()
rx = receiver.Receiver()

# main loop
while (True):

    # if the system is activated
    if app.on_activate():
        
        # call the receiver to analyse current audio inpu
        data, status = rx.read_frame(log = True)
        
        # pass the analyse result to the app
        app.handle_status(data, status)
        
        # update the spectrum
        spectrum = rx.get_fft()
        app.update_spectrum(spectrum)
        
        # update the text area
        if status == 5:
            app.update_text(rx.get_received_data())
    
    # update the UI
    app.update_ui()






