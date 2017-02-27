from openframeworks import *
from protopixel import Content

from OSC import OSCClient, OSCMessage

OSC_DEST_IP = "localhost"
OSC_DEST_PORT = 3334

content = Content('Custom OSC Sending Script')

# To send OSC messages we need an OSC Client
oscclient = OSCClient()

def update():
	message = OSCMessage() #Create the OSC Message
	message.setAddress("/myoscaddress") #Define the OSC Address
	message.append(44) #first argument
	message.append(11) #second argument
	message.append(4.5) #third argument
	oscclient.sendto(message,(OSC_DEST_IP,OSC_DEST_PORT)) #send osc message

