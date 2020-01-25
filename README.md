# Single Channel LoRaWAN Gateway

This repository contains a proof-of-concept implementation of a single
channel LoRaWAN gateway.

It has been tested on the Raspberry Pi platform, using a Semtech SX1272
transceiver (HopeRF RFM92W), and SX1276 (HopeRF RFM95W).

The code is for testing and development purposes only, and is not meant
for production usage.

Part of the source has been copied from the Semtech Packet Forwarder
(with permission).

Maintainer: [Thomas Telkamp](thomas@telkamp.eu)

Was forked by [@jlesech](https://github.com/tftelkamp/single_chan_pkt_fwd) to add json configuration file
then forked by [@hallard](https://github.com/hallard/single_chan_pkt_fwd)
then forked by [@adafruit](https://github.com/adafruit/single_chan_pkt_fwd) to add python scripting

The gateway can either be run as a service (using `sudo make install`), or run with a python frontend that also updates status messages to an attached OLED display.

## Added new Features

- added back single_chan_pkt_fwd.service for systemd (debian jessie minimal) start
- added `make install` and `make uninstall` into Makefile to install service

## Pin Mapping

Pin mapping used in `global_conf.json` follows WiringPi numbering (wPi colunm).

```bash
pi@raspberrypi:~ $ gpio readall
 +-----+-----+---------+------+---+---Pi 3B+-+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 | ALT0 | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 | ALT0 | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 0 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 1 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 1 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 3B+-+---+------+---------+-----+-----+
```

Pin configuration for using the Adafruit module:

```json
    "pin_nss": 11,
    "pin_dio0": 5,
    "pin_rst": 6
```

## Installation

Install dependencies:

- [wiringpi](http://wiringpi.com) (Now comes pre-installed in Raspbian)
- [circuitpython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
- [Adafruit SSD1306 python module](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)

Build project:

```bash
cd /home/pi
git clone https://github.com/markpatterson27/single_chan_pkt_fwd
make
```

### Run as service

To run the gateway as a service, use `sudo make install`.

```bash
sudo make install
```

To start service (should already be started at boot if you done make install and rebooted of course), stop service or look service status

```bash
systemctl start single_chan_pkt_fwd
systemctl stop single_chan_pkt_fwd
systemctl status single_chan_pkt_fwd
```

To see gateway log in real time

```bash
journalctl -f -u single_chan_pkt_fwd
```

### Run as python script

To run the gateway from the python script, just run the python script.

```bash
python3 lorawan_gateway.py
```

## License

The source files in this repository are made available under the Eclipse Public License v1.0, except:

- base64 implementation, that has been copied from the Semtech Packet Forwarder;
- RapidJSON, licensed under the MIT License.
