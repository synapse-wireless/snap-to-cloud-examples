# Cloud Examples

This project uses the SN171 Protoboard and a standard SNAP Connect
gateway running with tornado as webserver/scheduler to push data to different cloud services.

The application server for these examples uses the SNAP Connect Python library to communicate over a SNAP bridge
device to the wireless sensor nodes, and the Tornado Python library to communicate with a remote API. Both the SNAP 
Connect Python library and the Tornado Python library are high-performance asynchronous services, and they work 
really well together.

## AWS IoT Example
### Python Requirements
Note: You must be using python 2.7.11+ in order to use this example.

Install the package dependencies:
```pip install -r aws_iot/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/```

### AWS Requirements
An AWS developer account is required, your account must have full AWS IoT privileges. [Follow the instructions here to sign up for AWS.](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html#cli-signup)

You must install and authenticate with AWS CLI, this is a python package that is installed when you install the Python
requirements file.

To authenticate your user with AWS, type ```aws configure``` and specify your AWS Access Key ID, AWS Secret Access Key, 
and region. For more information, see [Configuring the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

Update the ```THINGS``` variable in ```aws_iot/settings.py``` file to specify your device IDs (these need be the SNAP 
addresses of your SN171 boards). Once you have updated this file, run ```python setup_aws.py``` from the ```aws_iot```
directory to create your devices, policy, and certificate.

### Running
Run the AWS example using the following command:
```python aws_iot_example.py```

## Exosite Example
### Python Requirements
The application is written for Python 2.7. Install the required libraries into your Python environment as follows:
```pip install -r requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/```

### Exosite Requirements
An Exosite "Portals" account is required. [Sign up for a free account here](https://portals.exosite.com/signup?plan=2692704445)
