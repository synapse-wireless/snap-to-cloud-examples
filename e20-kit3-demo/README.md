This project uses the SN171 Protoboard and a standard SNAP Connect
gateway running with tornado as webserver/scheduler to push data to Exosite.

The application server for this example is a standalone Python program.
It uses the SNAP Connect Python library to communicate over a SNAP bridge
device to the wireless sensor nodes, and the Tornado Python library to
communicate with the Exosite HTTP API. Both of these libraries are
high-performance asynchronous services, and they work really well together.

The application is written for Python 2.7. Install the required libraries
into your Python environment as follows:

pip install -r requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/

An Exosite "Portals" account is required. Sign up for a free account at:

https://portals.exosite.com/signup?plan=2692704445
