[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)
# E20 Example - Interfacing to Exosite's "Portals"

## Configuring Exosite Portals
To use this example a free Exosite Portal is required. To sign up visit:

> https://portals.exosite.com/signup?plan=2692704445

From the welcome screen choose Add a Device:

![](https://cloud.githubusercontent.com/assets/1317406/12903053/6f1e82f0-ce8a-11e5-97b9-1f54b3b3c5d4.png)
 
In the dialog that appears, choose "I want to create a generic device":

![](https://cloud.githubusercontent.com/assets/1317406/12903056/73f8c2cc-ce8a-11e5-9f35-204d16a8a532.png)
 
On the next step, "Device Setup", please fill any details that you want. In the final step it will ask for a name, which can be anything (such as "SN171"). Once the setup has completed, it should list your device in the devices table:

![](https://cloud.githubusercontent.com/assets/1317406/12903062/787d2efa-ce8a-11e5-97c6-5ac6b62a8c0a.png)

Click the newly added SN171 device and its details should be displayed:

![](https://cloud.githubusercontent.com/assets/1317406/12903065/7bc079c8-ce8a-11e5-9d7b-b6e22de2c818.png)
 
In the "Alias" text box, fill in the SNAP address of the module that is installed in the first SN171 board.

**NOTE** - to be compatible with the main.py example code, the addresses should be entered without any separators (no "." Or ":", etc.) plus the hexadecimal digits a-f must be entered in lower case.

Where the CIK value is displayed, copy this somewhere for later pasting into the CIK dictionary in main.py.

Next choose "Add Data" to define the information the SNAP node will be sending. 
In the "Data Setup" dialog that is displayed, fill in the values:

    "Data Source Name" = "Battery"
    "Data Source Format" = "integer"
    "Unit" = "mV"
    "Alias" = batt

The dialog should now look like this:

![](https://cloud.githubusercontent.com/assets/1317406/12903068/7f5ff6e4-ce8a-11e5-97d3-a68182574faa.png)
 
Submit this form and add two more data sources:

    "Data Source Name" = "Button Count"
    "Data Source Format" = "integer"
    "Unit" = "presses"
    "Alias" = count
    "Data Source Name" = "Button State"
    "Data Source Format" = "integer"
    "Unit" = ""
    "Alias" = state

## Setup Gateway
Simply power up the E20 and load the software onto the E20 (put it in the snap user directory).  You must edit the provided main.py file to change the EXOSITE_CIKS dictionary to match your SN171 MAC addresses and Exosite CIKs. Find the following code snippet and update it:

```python
# TODO: Replace these with values from your own Exosite account and resource
# We want to map SN171 SNAP addresses to Exosite CIKs
EXOSITE_CIKS = {"XXXXXX": 'unique Exosite CIK here',
                "YYYYYY": 'another unique Exosite CIK here'}
```

This example also uses several 3rd-part Python libraries. Install them onto your E20 using

```bash
sudo pip2.7.9 install -r requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/
```

Once both of these steps have been competed, execute the main.py Python script as sudo.  

```bash
sudo python2.7.9 main.py
```

Now that Exosite and the E20 have been configured, refreshing the "Device Information" on the Exosite website should show new values that were transmitted by the SNAP node.

Repeat the same process of adding a device and data sources for the other SN171.

Now take some time to explore Exosite's Portals website by creating your own dashboards.
