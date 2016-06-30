[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# E20 Example - Interfacing to Amazon AWS IoT

## Common Setup
Each example in this repo requires some amount of common setup. Please follow the
[common setup instructions](../README.md#common-setup) first.

## Configuring Amazon AWS IoT
To use this example, an AWS developer account is required, and your account must have full AWS IoT privileges. To sign up, visit:

> http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html#cli-signup

You must install and authenticate with AWS CLI; this is a Python package that is installed when you install the Python
requirements file.

## Setup Gateway
**Note:** You must be using Python 2.7.9+ in order to use this example.

Simply power up the E20 and load the software onto the E20 (put it in the snap user directory).

This example also uses several 3rd-party Python libraries. Install them onto your E20 using

```bash
sudo pip2.7.9 install -r aws_iot/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/
```

To authenticate your user with AWS, type ```/usr/local/lib/python2.7.9/bin/aws configure``` and specify your AWS Access Key ID, 
AWS Secret Access Key, and region. For more information, see [Configuring the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

Update the ```THINGS``` variable in ```aws_iot/settings.py``` file to specify your device IDs (these need be the SNAP 
addresses of your SN171 boards). Once you have updated this file, run ```python2.7.9 setup_aws.py``` from the ```aws_iot```
directory to create your devices, policy, and certificate.

Run the AWS example using the following command:

```bash
sudo python2.7.9 aws_iot_example.py
```
