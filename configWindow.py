
from tkinter import *
from tkinter import messagebox
import sounddevice as sd
from xml.dom import minidom
import xml.etree.ElementTree as ET
import mainWindow
import ipaddress

class configWindow:
    T = Entry
    T2 = Entry
    def __init__(self,root, principal):
        self.newWindow = Toplevel(root)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinat = int((screen_width/2) - (300/2))
        y_cordinat = int((screen_height/2) - (210/2))
        self.principal = principal
        self.selection = principal.c
        self.device = principal.d
        self.options = sd.query_devices()
        self.options = [d['name'] for d in self.options]
        self.clicked = StringVar()
  
# initial menu text
        self.clicked.set( self.options[self.principal.d] )
  
#Create Dropdown menu
        #drop = OptionMenu( root , clicked , *options )
        #drop.pack()
        self.newWindow.geometry("{}x{}+{}+{}".format(300, 240, x_cordinat, y_cordinat))
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Configuración")
    
        Label(self.newWindow,text ="Numero de Canales: ").pack()

        channels = ["1","8","16","32","48","64"]
        variable = StringVar()
        for x in channels:
            if x == str(self.principal.c):
                variable.set(x)
                break
        
        self.Channelsdrop = OptionMenu( self.newWindow , variable ,self.clicked , *channels, command=self.channelsSelected)
        self.Channelsdrop.pack()

        Label(self.newWindow,text ="Dispositivo").pack()
        Channelsdrop2 = OptionMenu( self.newWindow , self.clicked , *self.options, command=self.dispSelected )
        Channelsdrop2.pack()

        Label(self.newWindow,text ="Dirección IP").pack()
        self.T = Entry(self.newWindow)
        self.T.insert(0,self.principal.ip)
        self.T.pack()

        Label(self.newWindow,text ="Puerto").pack()
        self.T2 = Entry(self.newWindow)
        self.T2.insert(0,self.principal.puer)
        self.T2.pack()

        self.newWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        widget2 = Button(self.newWindow, text='Guardar', command=self.guess)
        widget2.pack()
    
    def on_closing(self):
        self.principal.isConfigOpen = False
        self.newWindow.destroy()

    def channelsSelected(self,selection):
        print(selection)
        self.selection = int(selection)
        
    def dispSelected(self,selection):
        print(selection)
        for indx , x in enumerate(self.options):
            if x == selection:
                self.device = indx
                break

    def guess(self):
        if self.T.get() != "" and self.T2.get() != "":
            xml_tree = ET.parse("data.xml")
            scalars = xml_tree.findall('.//models')
            scalars[0].find('ip').text = self.T.get()
            scalars[0].find('puerto').text = self.T2.get()
            scalars[0].find('canales').text = str(self.selection)
            scalars[0].find('dispositivo').text = str(self.device)
            try:
                ipobject = ipaddress.ip_address(self.T.get())
                puerto = int(self.T2.get())
                ET.dump(xml_tree)
                xml_tree.write('data.xml')
                self.principal.readData()
                self.principal.isConfigOpen = False
                self.newWindow.destroy()
            except ValueError:
                messagebox.showerror(title='Error',message='Ip o Puerto Incorrectos')
        else:
            messagebox.showwarning(title='Error',message='Faltan datos por llenar')