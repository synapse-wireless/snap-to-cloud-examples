The application server for this example is a standalone python program.
It uses the SNAP Connect python library to communicate over a SNAP bridge
device to the wireless sensor nodes, and the Tornado python library to
serve HTTP and Websocket connections to browsers. Both of these libraries
are high-performance asynchronous services, and they work really well
together.

The application is written for Python 2.7. Install the required libraries
into your python environment as follows:

pip install snapconnect -i https://update.synapse-wireless.com/pypi/
pip install tornado
