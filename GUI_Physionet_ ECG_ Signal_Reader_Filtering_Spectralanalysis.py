# GUI_Physionet_-ECG_-Signal_Reader_Filtering_Spectralanalysis
# Editor: Philip Schmidt
# Date: 09/20/2020
# Detailed script documentation in form of comments right next to the code

# Enjoy using the program!

# Installing and upgrading all necessary packages
from subprocess import call
my_packages = ['matplotlib', 'scipy', 'numpy==1.17.4']
def upgrade(package_list):
    call(['pip', 'install', '--upgrade', '--user'] + package_list)
upgrade(my_packages)

# import of libraries
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure

import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.filedialog

from math import pi
import scipy.fftpack as sf
import scipy.signal as sig 


LARGE_FONT= ("Verdana", 12)



class window(tk.Tk):
    
    def __init__(self):
        
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "GUI Physionet ECG Signal Reader with advanced Filtering and Spectralanalysis")
        
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    
        
class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Welcome", font=("Verdana", 16))
        label.pack(pady=10,padx=10)

        self.pack(expand=True, fill='both')

        ttk.Button(self, text="Display ECG Data", command =lambda: self.read_in_data()).pack(pady=5,padx=10)

        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=5,padx=10)
        
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=5,padx=10)

        label = tk.Label(self, text="Display, analyze and filter any ECG signal by clicking the buttons above!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        

    def read_in_data(self):
        ecg_path = tkinter.filedialog.askopenfilename()
        ecg_data = np.fromfile(ecg_path, dtype=int)

        fs = 360
        time = np.arange(ecg_data.size) / fs
        my_label = Label(self, text='File path: ' + ecg_path).pack()


        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(111)
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 10)
        a.plot(time, ecg_data)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        
    
class Analyzer(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Analyzer", font=("Verdana", 16))
        label.pack(pady=10,padx=10)

        ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).pack(pady=5,padx=10)
      
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=5,padx=10)
        label = tk.Label(self, text="The powerspectrum of the generated ECG signal is analyzed here!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        self.spectral_analysis()

    

    def spectral_analysis(self):
        # Plotting ECG
        Fs = 360
        t = 4
        f = 10

        ecg_path = tkinter.filedialog.askopenfilename()
        x = np.fromfile(ecg_path, dtype=int)
        x = (x - 1024) / 200.0
        my_label = Label(self, text='File path: ' + ecg_path).pack()

        
        n = np.arange(x.size) / Fs
        

        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(211)
        
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.plot(n, x)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #Spectral Analysis
        x_fft = abs(sf.fft(x))
        l = np.size(x)
        fr = (Fs/2)*np.linspace(0, 1, l/2)                  
        x_magnitude = (2 / l)* abs(x_fft[0:np.size(fr)])

        f2 = Figure(figsize=(10,6), dpi=100)
        b = f.add_subplot(212)
        
        b.set_xlabel('Frequency / Hz')
        b.set_ylabel('Magnitude / dB')
        b.set_title("Spectral analysis of the ECG")
        
        b.plot(fr, 100000*x_magnitude)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.tight_layout()
        f2.tight_layout()




class Filters(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Filters", font=("Verdana", 16))
        label.pack(pady=10,padx=10)

        ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(StartPage)).pack(pady=5,padx=10)
      
        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=5,padx=10)

        ttk.Button(self, text="High Pass Filtering", 
            command=lambda: master.switch_frame(Highpass_Filter)).pack(pady=3,padx=10)

        ttk.Button(self, text="Low Pass Filtering", 
            command=lambda: master.switch_frame(Lowpass_Filter)).pack(pady=3,padx=10)

        ttk.Button(self, text="Band Pass Filtering",
            command=lambda: master.switch_frame(Bandpass_Filter)).pack(pady=3,padx=10)

        ttk.Button(self, text="Band Stop Filtering",
            command=lambda: master.switch_frame(Bandstop_Filter)).pack(pady=3,padx=10)

        label = tk.Label(self, text="This is the ECG we are going to filter! Please select your filter :)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
    

class Bandpass_Filter(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Band Pass Filtering", font=("Verdana", 16))
        label.pack(pady=10,padx=10) 

        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=3,padx=10)
      
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=3,padx=10)

        Lower_CutoffFrequency = tk.simpledialog.askfloat("Lower CutoffFrequency", "Which lower Cut off Frequency do you want?") 
        Upper_CutoffFrequency = tk.simpledialog.askfloat("Upper CutoffFrequency", "Which upper Cut off Frequency do you want?") 
        Ordernumber = tk.simpledialog.askinteger("Ordernumber", "Which Ordernumber do you want?") 

        label_1 = tk.Label(self, text="Lower Cut off Frequency / Hz")                  # nice way of sorting widgets and grid to type in text :)
        label_1.pack(padx=2, pady=2)
        label_1_1 = tk.Label(self, text=Lower_CutoffFrequency)                  # nice way of sorting widgets and grid to type in text :)
        label_1_1.pack(padx=2, pady=2)

        label_1 = tk.Label(self, text="Upper Cut off Frequency / Hz")                  
        label_1.pack(padx=2, pady=2)
        label_1_1 = tk.Label(self, text=Upper_CutoffFrequency)                  
        label_1_1.pack(padx=2, pady=2)
        
        label_2 = tk.Label(self, text="Ordernumber")
        label_2.pack(padx=2, pady=2)
        label_2_1 = tk.Label(self, text=Ordernumber)
        label_2_1.pack(padx=2, pady=2)

        self.Bandpass_Filter(Lower_CutoffFrequency, Upper_CutoffFrequency, Ordernumber)

    def Bandpass_Filter(self, Lower_CutoffFrequency, Upper_CutoffFrequency, Ordernumber):
        
        matplotlib.pyplot.close('all')
        # Design Band Pass Filter 
        Fs = 360
        
        ecg_path = tkinter.filedialog.askopenfilename()
        x = np.fromfile(ecg_path, dtype=int)
        n = np.arange(x.size) / Fs
        
        filter_order = Ordernumber                                        # Changeable FilterOrder
        cut_off_f = np.array([Lower_CutoffFrequency , Upper_CutoffFrequency])         # Cut off Frequency!!!!
        normalized= 2*cut_off_f / Fs
        [b,c] = sig.butter(filter_order, normalized, btype = 'bandpass')

        # filterresponse

        [W,h] = sig.freqz(b,c, worN = 1024)
        W = Fs * W / (2 * pi)

        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(311)
        
        a.set_xlabel('Frequency / Hz')
        a.set_ylabel("Magnitude / dB")
        a.set_title('Band Pass Filter Frequency Response')
       
        a.plot(W, 20 * np.log10(h))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bandpass filtered signal

        x_filtered = sig.lfilter(b, c, x)

        f2 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(312)
        
        a.set_xlabel('Time / s')
        a.set_ylabel("Amplitude / mV")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.set_title('Band Pass Filtered ECG')
       
        a.plot(n, x_filtered)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        Fs = 360
        
        n = np.arange(x.size) / Fs
        
        f3 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(313)
        
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.plot(n, x)

        canvas = FigureCanvasTkAgg(f3, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        f.tight_layout()
        f2.tight_layout()
        f3.tight_layout()


class Highpass_Filter(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="High Pass Filtering", font=("Verdana", 16))
        label.pack(pady=10,padx=10) 

        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=3,padx=10)
      
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=3,padx=10)

        CutoffFrequency = tk.simpledialog.askfloat("CutoffFrequency", "Which Cut off Frequency do you want?") 
        Ordernumber = tk.simpledialog.askinteger("Ordernumber", "Which Ordernumber do you want?") 

        label_1 = tk.Label(self, text="Cut off Frequency / Hz")                  # nice way of sorting widgets and grid to type in text :)
        label_1.pack(padx=2, pady=2)
        label_1_1 = tk.Label(self, text=CutoffFrequency)                  # nice way of sorting widgets and grid to type in text :)
        label_1_1.pack(padx=2, pady=2)
        
        label_2 = tk.Label(self, text="Ordernumber")
        label_2.pack(padx=2, pady=2)
        label_2_1 = tk.Label(self, text=Ordernumber)
        label_2_1.pack(padx=2, pady=2)
        
        
        self.Highpass_Filter(CutoffFrequency, Ordernumber)

    def Highpass_Filter(self, CutoffFrequency, Ordernumber):
        
        # Design Highpass Filter 
        Fs = 360
        ecg_path = tkinter.filedialog.askopenfilename()
        x = np.fromfile(ecg_path, dtype=int)
        n = np.arange(x.size) / Fs
        
        filter_order = Ordernumber                                        # Changeable FilterOrder
        cut_off_f = np.array([ CutoffFrequency ])                         # Cut off Frequency!!!!
        normalized= 2*cut_off_f / Fs
        [b,c] = sig.butter(filter_order, normalized, btype = 'highpass')

        # filterresponse

        [W,h] = sig.freqz(b,c, worN = 1024)
        W = Fs * W / (2 * pi)

        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(311)
        
        a.set_xlabel('Frequency / Hz')
        a.set_ylabel("Magnitude / dB")
        a.set_title('High Pass Filter Frequency Response')
       
        a.plot(W, 20 * np.log10(h))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Highpass filtered signal

        x_filtered = sig.lfilter(b, c, x)

        f2 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(312)
        
        a.set_xlabel('Time / s')
        a.set_ylabel("Amplitude / mV")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.set_title('High Pass Filtered ECG')
       
        a.plot(n, x_filtered)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        f3 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(313)
        
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.plot(n, x)

        canvas = FigureCanvasTkAgg(f3, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        f.tight_layout()
        f2.tight_layout()
        f3.tight_layout()


class Lowpass_Filter(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Low Pass Filtering", font=("Verdana", 16))
        label.pack(pady=10,padx=10) 

        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=3,padx=10)
      
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=3,padx=10)

        CutoffFrequency = tk.simpledialog.askfloat("CutoffFrequency", "Which Cut off Frequency do you want?") 
        Ordernumber = tk.simpledialog.askinteger("Ordernumber", "Which Ordernumber do you want?") 

        label_1 = tk.Label(self, text="Cut off Frequency / Hz")                  # nice way of sorting widgets and grid to type in text :)
        label_1.pack(padx=2, pady=2)
        label_1_1 = tk.Label(self, text=CutoffFrequency)                  # nice way of sorting widgets and grid to type in text :)
        label_1_1.pack(padx=2, pady=2)
        
        label_2 = tk.Label(self, text="Ordernumber")
        label_2.pack(padx=2, pady=2)
        label_2_1 = tk.Label(self, text=Ordernumber)
        label_2_1.pack(padx=2, pady=2)
        

        self.Lowpass_Filter(CutoffFrequency, Ordernumber)

    def Lowpass_Filter(self, CutoffFrequency, Ordernumber):
        
        # Design Lowpass Filter 
        Fs = 360
        ecg_path = tkinter.filedialog.askopenfilename()
        x = np.fromfile(ecg_path, dtype=int)
        n = np.arange(x.size) / Fs
        
        filter_order = Ordernumber                                        # Changeable FilterOrder
        cut_off_f = np.array([ CutoffFrequency ])                         # Cut off Frequency!!!
        normalized= 2*cut_off_f / Fs
        [b,c] = sig.butter(filter_order, normalized, btype = 'lowpass')

        # filterresponse

        [W,h] = sig.freqz(b,c, worN = 1024)
        W = Fs * W / (2 * pi)

        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(311)
        
        a.set_xlabel('Frequency / Hz')
        a.set_ylabel("Magnitude / dB")
        a.set_title('Low Pass Filter Frequency Response')
       
        a.plot(W, 20 * np.log10(h))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Highpass filtered signal

        x_filtered = sig.lfilter(b, c, x)

        f2 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(312)
        
        a.set_xlabel('Time / s')
        a.set_ylabel("Amplitude / mV")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.set_title('Low Pass Filtered ECG')
       
        a.plot(n, x_filtered)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        f3 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(313)
        
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.plot(n, x)

        canvas = FigureCanvasTkAgg(f3, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        f.tight_layout()
        f2.tight_layout()
        f3.tight_layout()

class Bandstop_Filter(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Band Stop Filtering", font=("Verdana", 16))
        label.pack(pady=10,padx=10) 

        ttk.Button(self, text="Analyzer", command=lambda: master.switch_frame(Analyzer)).pack(pady=3,padx=10)
      
        ttk.Button(self, text="Filters", command=lambda: master.switch_frame(Filters)).pack(pady=3,padx=10)

        Lower_CutoffFrequency = tk.simpledialog.askfloat("Lower CutoffFrequency", "Which lower Cut off Frequency do you want?") 
        Upper_CutoffFrequency = tk.simpledialog.askfloat("Upper CutoffFrequency", "Which upper Cut off Frequency do you want?") 
        Ordernumber = tk.simpledialog.askinteger("Ordernumber", "Which Ordernumber do you want?") 

        label_1 = tk.Label(self, text="Lower Cut off Frequency / Hz")                  # nice way of sorting widgets and grid to type in text :)
        label_1.pack(padx=2, pady=2)
        label_1_1 = tk.Label(self, text=Lower_CutoffFrequency)                  # nice way of sorting widgets and grid to type in text :)
        label_1_1.pack(padx=2, pady=2)

        label_1 = tk.Label(self, text="Upper Cut off Frequency / Hz")                  
        label_1.pack(padx=2, pady=2)
        label_1_1 = tk.Label(self, text=Upper_CutoffFrequency)                  
        label_1_1.pack(padx=2, pady=2)
        
        label_2 = tk.Label(self, text="Ordernumber")
        label_2.pack(padx=2, pady=2)
        label_2_1 = tk.Label(self, text=Ordernumber)
        label_2_1.pack(padx=2, pady=2)

        self.Bandstop_Filter(Lower_CutoffFrequency, Upper_CutoffFrequency, Ordernumber)


    def Bandstop_Filter(self, Lower_CutoffFrequency, Upper_CutoffFrequency, Ordernumber):
        
        # Design Highpass Filter 
        Fs = 360
        ecg_path = tkinter.filedialog.askopenfilename()
        x = np.fromfile(ecg_path, dtype=int)
        n = np.arange(x.size) / Fs
        
        filter_order = Ordernumber                                        # Changeable FilterOrder
        cut_off_f = np.array([Lower_CutoffFrequency, Upper_CutoffFrequency])   # Cut off Frequency!!!!
        normalized= 2*cut_off_f / Fs
        [b,c] = sig.butter(filter_order, normalized, btype = 'bandstop')

        # filterresponse

        [W,h] = sig.freqz(b,c, worN = 1024)
        W = Fs * W / (2 * pi)

        f = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(311)
        
        a.set_xlabel('Frequency / Hz')
        a.set_ylabel("Magnitude / dB")
        a.set_title('Band Stop Filter Frequency Response')
       
        a.plot(W, 20 * np.log10(h))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bandstop filtered signal

        x_filtered = sig.lfilter(b, c, x)

        f2 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(312)
        
        a.set_xlabel('Time / s')
        a.set_ylabel("Amplitude / mV")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.set_title('band stop filtered ECG')
       
        a.plot(n, x_filtered)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        f3 = Figure(figsize=(10,6), dpi=100)
        a = f.add_subplot(313)
        
        a.set_xlabel("time in s")
        a.set_ylabel("ECG in mV")
        a.set_title("ECG Signal")
        a.set_xlim(0, 20)
        #a.set_ylim(-2, 1.5)
        a.plot(n, x)

        canvas = FigureCanvasTkAgg(f3, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        f.tight_layout()
        f2.tight_layout()
        f3.tight_layout()


app = window()
app.mainloop()
