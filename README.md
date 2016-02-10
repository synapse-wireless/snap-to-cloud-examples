[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# E20 Example - Interfacing to Cloud Services

This example allows you to stand up a full "node to cloud" data monitoring solution. It showcases the following products (for example, from a Synapse EK5100 kit):

- 1 x SNAP Connect E20
    - Using DHCP on the Ethernet Port for Internet access
    - Using the internal SNAP node for SNAP Network access
- 2 x SN171 Prototyping boards with RF200 modules installed
- 1 x SN132 USB SNAP Stick
- Synapse's Portal software
- A cloud IoT service, like:
    - Amazon AWS IoT
    - Adafruit IO
    - Exosite's Portals
    - Initial State

The application server for these examples uses the SNAP Connect Python library to communicate over a SNAP bridge
device to the wireless sensor nodes, and the Tornado Python library to communicate with a remote API. Both the SNAP 
Connect Python library and the Tornado Python library are high-performance asynchronous services, and they work 
really well together.

## Common Setup
These setup steps are common to all of the examples included here, regardless of the cloud service used.

**NOTE** - If you have already run the ["Gateway-Hosted Web Server"](https://github.com/synapse-wireless/e20-gateway-hosted-webserver/) demo, some of these steps have already been completed.

### Setup SN132
Connect the SN132 to your PC by plugging it into any available USB port.

### Setup Portal
If you have not already done so, download and install the Synapse Portal IDE.

The Synapse Portal IDE will allow complete embedded module development, as well as wireless sniffer capability – download the latest version here: 

> https://forums.synapse-wireless.com/showthread.php?t=9

### Setup the SN171s
Copy the contents of this project's `snappyImages` directory to your `Portal/snappyImages` directory. Apply power to the SN171s.

Now you can connect Portal to the SN132 as a bridge node and upload the `demo_sn171.py` script into the SN171s.

Please make a note of the SNAP Addresses of the two SN171 nodes - you will need this information later.

## Install Python 2.7.9
The E20 runs Ubuntu 14.04, which comes with Python 2.7.6 by default. Python 2.7.9 or later is required for interacting with 
AWS IoT and Exosite, so we need to build it for the E20. If you do not already have Python 2.7.9 installed, clone this project
onto the E20 and run ```sudo ./install-python2.7.9.sh``` to build and install it.

## Instructions for the Different Cloud Services

Follow the instructions contained in the README files in each cloud service's directory to get started:

| Cloud Service   | Instructions                                     |
|-----------------|--------------------------------------------------|
| Adafruit IO     | [adafruitio/README.md](adafruitio/README.md)     |
| Amazon AWS IoT  | [aws_iot/README.md](aws_iot/README.md)           |
| Exosite Portals | [exosite/README.md](exosite/README.md)           |
| Initial State   | [initialstate/README.md](initialstate/README.md) |

<!-- meta-tags: vvv-e20, vvv-sn171, vvv-sn132, vvv-rf200, vvv-ek5100, vvv-snapconnect, vvv-initialstate, vvv-aws-iot, vvv-exosite, vvv-adafruitio, vvv-js, vvv-html, vvv-python, vvv-example -->
