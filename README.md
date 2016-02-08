![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)

# E20 Example - Interfacing to Cloud Services

This example allows you to stand up a full "node to cloud" data monitoring solution. It showcases the following products (for example, from a Synapse EK5100 kit):

- 1 x SNAP Connect E20
    - Using DHCP on the Ethernet Port for Internet access
    - Using the internal SNAP node for SNAP Network access
- 2 x SN171 Prototyping boards with RF200 modules installed
- 1 x SN132 USB SNAP Stick
- Synapse's Portal software
- A cloud IoT service, like:
    - Exosite's Portals
    - Amazon AWS IoT
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

Please make a note of the SNAP Addresses of the two SN171 nodes - you will need this information later

## Install Python 2.7.9
The E20 runs Ubuntu 14.04, which comes with Python 2.7.6 by default. Python 2.7.9 or later is required for interacting with 
AWS IoT and Exosite, so we need to build it for the E20. If you do not already have Python 2.7.9 installed, clone this project
onto the E20 and run ```sudo ./install-python2.7.9.sh``` to build and install it.

## AWS IoT Example
### Python Package Requirements
Note: You must be using python 2.7.9+ in order to use this example.

Install the package dependencies:
```sudo pip2.7.9 install -r aws_iot/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/```

### AWS Requirements
An AWS developer account is required, your account must have full AWS IoT privileges. [Follow the instructions here to sign up for AWS.](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html#cli-signup)

You must install and authenticate with AWS CLI, this is a python package that is installed when you install the Python
requirements file.

To authenticate your user with AWS, type ```/usr/local/lib/python2.7.9/bin/aws configure``` and specify your AWS Access Key ID, 
AWS Secret Access Key, and region. For more information, see [Configuring the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

Update the ```THINGS``` variable in ```aws_iot/settings.py``` file to specify your device IDs (these need be the SNAP 
addresses of your SN171 boards). Once you have updated this file, run ```python2.7.9 setup_aws.py``` from the ```aws_iot```
directory to create your devices, policy, and certificate.

### Running
Run the AWS example using the following command:
```sudo python2.7.9 aws_iot_example.py```

## Exosite Example
### Python Requirements
The application is written for Python 2.7. Install the required libraries into your Python environment as follows:
```sudo pip2.7.9 install -r exosite/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/```

### Exosite Requirements
An Exosite "Portals" account is required. [Sign up for a free account here](https://portals.exosite.com/signup?plan=2692704445)

See `exosite-demo.docx` for instructions on how to add devices to your Exosite "Portals" account.

### Running
Run the Exosite example using the following command:
```sudo python2.7.9 exosite_example.py```

## Initial State Example
### Python Requirements
The application is written for Python 2.7. Install the required libraries into your Python environment as follows:
```sudo pip2.7.9 install -r initialstate/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/```

### Initial State Requirements
To use this example a free Initial State login is required. To sign up, visit:
https://www.initialstate.com/app#/register

See [initialstate/README.md](initialstate/README.md) for instructions on how to set up your Initial State account.

### Running
Run the Initial State example using the following command:
```sudo python2.7.9 initialstate_example.py```
