import sounddevice as sd
import mainWindow
options = [
]
def optionsMenu():
    g = sd.query_devices()
    print(sd.query_devices())
    print([d['name'] for d in g])
optionsMenu()

#def show():
    #label.config( text = clicked.get() )
  
# Dropdown menu options
#options = sd.query_devices()
#options = [d['name'] for d in options]
#clicked = StringVar()
  
# initial menu text
#clicked.set( options[0] )
  
# Create Dropdown menu
#drop = OptionMenu( root , clicked , *options )
#drop.pack()
# Create Label
principal = mainWindow.MainWindow()