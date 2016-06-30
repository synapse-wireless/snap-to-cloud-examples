[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# E20 Example - Interfacing to Initial State

## Common Setup
Each example in this repo requires some amount of common setup. Please follow the
[common setup instructions](../README.md#common-setup) first.

## Configuring Initial State
To use this example, a free Initial State login is required. To sign up, visit:

> https://www.initialstate.com/app#/register

From the welcome screen choose Create HTTPS Bucket:

![](https://cloud.githubusercontent.com/assets/1317406/12657821/0e6564dc-c5cb-11e5-8f02-1403b81565cf.png)
 
In the form that appears you can choose any name that you wish for the bucket. A possibility would be to use the node's SNAP address.

Once the bucket has been created you will need to find your Bucket and Access keys. To access these keys, click on the settings link:

![](https://cloud.githubusercontent.com/assets/1317406/12657827/162c6cce-c5cb-11e5-97ab-73675f626050.png)
 
You should see a panel like this:

![](https://cloud.githubusercontent.com/assets/1317406/12657839/1b091ff8-c5cb-11e5-86f2-0931295fc192.png)

Copy the "Bucket Key" and "Access Key" somewhere for later pasting into initialstate_connector.py.

## Setup Gateway
Simply power up the E20 and load the software onto the E20 (put it in the snap user directory).  You must edit the provided initialstate_connector.py file to change the INITIAL_STATE_BUCKETS dictionary to match your SN171 MAC addresses and Initial State keys. Find the following code snippet and update it:

```python
# TODO: Replace these with values from your own Initial State account and buckets
# We want to map Initial State buckets to nodes
INITIAL_STATE_BUCKETS = {
    "XXXXXX": "unique Initial State bucket key here",
    "YYYYYY": "another unique Initial State bucket key here"
}
ACCESS_KEY = "your unique access key here"
```

This example also uses several 3rd-part Python libraries. Install them onto your E20 using

```bash
sudo pip2.7.9 install -r initialstate/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/
```

Once both of these steps have been competed, execute the initialstate_example.py Python script as sudo.  

```bash
sudo python2.7.9 initialstate_example.py
```

Now that Initial State and the E20 have been configured, the Initial State website should show new values that were transmitted by the SNAP node.
Repeat the same process of adding a device and data sources for the other SN171.

Now take some time to explore Initial State's website by viewing data sent from your SN171s.
