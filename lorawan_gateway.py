"""
lorawan_gateway.py

Learn Guide: https://learn.adafruit.com/raspberry-pi-single-channel-lorawan-gateway
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import sys, json, time, subprocess, re, threading, uuid
# Import Adafruit Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Gateway id calculation (based off MAC address)
mac_addr = hex(uuid.getnode()).replace('0x', '')
print('Gateway ID: {0}:{1}:{2}:ff:ff:{3}:{4}:{5}'.format(mac_addr[0:2],mac_addr[2:4],
        mac_addr[4:6],mac_addr[6:8], mac_addr[8:10], mac_addr[10:12]))


def stats():
    """Prints information about the Pi
    to a display 
    """
    print('MODE: Pi Stats')
    # Clear Display
    display.fill(0)
    # Shell scripts for system monitoring from here :
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # Write text to display
    display.text("IP: "+str(IP), 0, 0, 1)
    display.text(str(CPU), 0, 15, 1)
    display.text(str(MemUsage), 0, 25, 1)
    # Display text for 5 seconds
    display.show()
    time.sleep(5)

def gateway():
    """Runs the Semtech Single Channel
    Packet Forwarder, sends output to
    a display.
    """
    print('MODE: Pi Gateway')
    # Clear Display
    display.fill(0)
    display.text("Starting Gateway...", 15, 0, 1)
    display.show()
    print('starting gateway...')
    proc = subprocess.Popen("./single_chan_pkt_fwd", bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
      print(proc.stdout.readline())
    proc.kill()

def gateway_info():
  """Displays information about the LoRaWAN gateway. 
  """
  print('MODE: Gateway Info')
  display.fill(0)
  display.show()
  # Import `global_conf.json`
  with open('global_conf.json', 'r') as config:
    gateway_config = json.load(config)
  # parse `SX127x_conf` 
  SX127x_conf = gateway_config['SX127x_conf']
  gateway_freq = SX127x_conf['freq']/1000000
  gateway_sf = SX127x_conf['spread_factor']
  # parse `gateway_conf`
  gateway_conf = gateway_config['gateway_conf']
  gateway_name = gateway_conf['name']
  # parse 'gateway_conf[servers]'
  server_list = gateway_conf['servers']
  ttn_server = server_list[0]
  ttn_server_addr = ttn_server['address']

  print('Server: ', ttn_server_addr[0:9])
  print('Freq: ', gateway_freq)
  print('SF: ', gateway_sf)
  print('Gateway Name:', gateway_name)
  # write 3 lines of text
  display.text(gateway_name, 15, 0, 1)
  display.text('{0} MHz, SF{1}'.format(gateway_freq, gateway_sf), 15, 10, 1)
  display.text('TTN: {0}'.format(ttn_server_addr[0:9]), 15, 20, 1)
  display.show()
  time.sleep(5)


while True:
    # draw a box to clear the image
    display.fill(0)

    display.text('LoRaWAN Gateway ID', 15, 0, 1)
    display.text('{0}:{1}:{2}:ff'.format(mac_addr[0:2], mac_addr[2:4],
                    mac_addr[4:6]), 25, 15, 1)
    display.text('ff:{0}:{1}:{2}'.format(mac_addr[6:8],mac_addr[8:10], 
                    mac_addr[10:12]), 25, 25, 1)

    # Radio Bonnet Buttons
    if not btnA.value:
        # show pi info
        stats()
    if not btnB.value:
        # start the gateway
        gateway()
    if not btnC.value:
        # show gateway configuration
        gateway_info()

    display.show()
    time.sleep(.1)