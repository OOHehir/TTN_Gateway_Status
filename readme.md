# The Things Network Gateway Status Script

This project is run on a Raspberry Pi with a RAK 7243.
It runs a python 3 script to perodically poll the TTN URL (http://noc.thethingsnetwork.org:8085/api/v2/gateways/eui-b827ebfffe87bd11) to check when the gateway was last seen.
Depending on the result it sets LED's to indicate the Gateway status

# Installation:
Install the .py file in your home folder & follow the instructions on the .service file to get it running
