from tkinter import *
from tkinter import messagebox
from xml.dom import minidom
import configWindow
import socket
import sounddevice as sd
import numpy as np
import threading as th

class MainWindow:
    dispositivo = 0
    canals = 0
    def __init__(self):
        self.master = Tk()
        self.isConfigOpen = False
        self.isRunning = False
        self.master.geometry("500x250")
        window_height = 200
        window_width = 350
        self.master.winfo_toplevel().title("Dante Mixer")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))  
        self.label = Label( self.master , text = "Numero de Canales: 32" )
        self.label.pack()
        self.label.place(relx=0.0,rely=0.1,anchor='nw')

        self.label2 = Label( self.master , text = "Dispositivo: 3" )
        self.label2.pack()
        self.label2.place(relx=0.0,rely=0.2,anchor='nw')

        self.label3 = Label( self.master , text = "IP Servidor: 192.168.1.144" )
        self.label3.pack()
        self.label3.place(relx=0.0,rely=0.3,anchor='nw')

        self.label4 = Label( self.master , text = "Puerto Servidor: 5001" )
        self.label4.pack()
        self.label4.place(relx=0.0,rely=0.4)

        self.widget = Button(self.master, text='Iniciar', command=self.begin)
        self.widget.pack()
        self.widget.place(relx=0.5,rely=0.7,anchor='center')

        self.widget2 = Button(self.master, text='Configuración', command=self.openNewWindow)
        self.widget2.pack()
        self.widget2.place(relx=0.8,rely=0.05, anchor='center')
        self.readData()
        self.master.mainloop()  

    def begin(self):
        if self.d != -1 and self.c != 0:
            if self.isConfigOpen == False:
                if self.isRunning == False:
                    self.isRunning = True
                    self.widget.config(text='Parar')
                    self.widget.config(bg='red')
                    self.setSocket()
                else :
                    
                    self.widget.config(text='Iniciar')
                    self.isRunning = False
                    print("as")
                    self.i.close()
                
        else:
            messagebox.showwarning(title='Error',message='Faltan datos por configurar')
    
    def openNewWindow(self):
        if self.isConfigOpen == False and self.isRunning == False:
            self.isConfigOpen = True
            y = configWindow.configWindow(self.master,self)

    def readData(self):
        file = minidom.parse('data.xml')
        self.ips = file.getElementsByTagName('ip')
        self.ip = self.ips[0].firstChild.data
        self.prots = file.getElementsByTagName('puerto')
        self.channels = file.getElementsByTagName('canales')
        self.device = file.getElementsByTagName('dispositivo')
        self.puer = self.prots[0].firstChild.data
        print(self.device[0].firstChild.data)
        print(self.channels[0].firstChild.data)
        self.label3.config(text="Ip Servidor: " + self.ips[0].firstChild.data)
        self.label4.config(text="Puerto Servidor: " + self.prots[0].firstChild.data)
        self.d = int(self.device[0].firstChild.data)
        self.c = int(self.channels[0].firstChild.data)
        if self.d == -1:
            self.label2.config(text="Dispositivo: No seleccionado")
        else:
            self.label2.config(text="Dispositivo: " + str(self.d))

        if self.c == 0:
            self.label.config(text="Numero de Canales: No seleccionado")
        else:
            self.label.config(text="Numero de Canales: " + str(self.c))

    def sonido(self):
            try:
                print("canal 1")
                Y = sd.InputStream(
                    channels=self.canales,
                    callback=self.audio_callback)
                self.i = Y
                with self.i:
                    print("dsf")
                    #while True:
                     #   print("a")

            except Exception as e:
                messagebox.showerror(title='error',message=e)
                self.widget.config(text='Iniciar')
                self.isRunning = False
                print(e)
    
    def setSocket(self):
        dispositivo =  self.d
        self.MCAST_GRP = str(self.ip)
        self.MCAST_PORT = int(self.puer)
        self.canales = self.c

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,2)
        sd.default.device = dispositivo
        sd.default.latency = 'low'
        sd.default.samplerate = 44100
        sd.default.dtype = 'int16'
        sd.default.blocksize = 64
        #sonido()

        self.sonido()
    
    def audio_callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        c = np.transpose(indata)
        h = np.concatenate(c,axis=0)
        #print("popo",np.sum(indata,axis=1),"popo")3
        print("po",np.sum(indata,axis=1),"po")
        #print('p')
        #h = np.sum(indata,axis=1)
        #tou=h.byteswap()
        #total=tou.tobytes()
        
        self.sock.sendto(h.tobytes(),(self.MCAST_GRP, self.MCAST_PORT))
        