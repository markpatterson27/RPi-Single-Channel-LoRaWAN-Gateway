Single Channel LoRaWAN Gateway
==============================
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

Installation
------------

Install dependencies 
- [wiringpi](http://wiringpi.com)

```shell
cd /home/pi
git clone https://github.com/hallard/single_chan_pkt_fwd
make
sudo make install
````

License
-------
The source files in this repository are made available under the Eclipse Public License v1.0, except:
- base64 implementation, that has been copied from the Semtech Packet Forwarder;
- RapidJSON, licensed under the MIT License.
 

