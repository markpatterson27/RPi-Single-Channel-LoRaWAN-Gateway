from network import LoRa 
import struct 
import binascii 
import socket 
from machine import Pin

freq = 902300000 
# Initialize LoRa in LORAWAN mode. 
lora = LoRa(mode=LoRa.LORAWAN) 
#Setup the single channel for connection to the gateway 
for channel in range(0, 72): 
   lora.remove_channel(channel) 
for chan in range(0, 8): 
   lora.add_channel(chan,  frequency=freq,  dr_min=0,  dr_max=3) 
#Device Address 
dev_addr = struct.unpack(">l", binascii.unhexlify('260210EF'))[0] 
#Network Session Key 
nwk_swkey = binascii.unhexlify('2B5F40BF17A407ACBC7463BBEB206FCB') 
#App Session Key 
app_swkey = binascii.unhexlify('749B1674F5D6E30A54B924BF655FE080') 
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey)) 
# create a LoRa socket 
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) 
# set the LoRaWAN data rate 
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3) 
# make the socket non-blocking 
s.setblocking(False)
p_in = Pin('G17', mode=Pin.IN, pull=Pin.PULL_UP)

prev_button = True

while True:
        button = p_in()
        if(button==0 and button != prev_button):
            print("button pressed")
            s.send('button pressed')
            prev_button = button
        if(button and button != prev_button):
            print("button released")
            s.send('button released')
            prev_button = button

