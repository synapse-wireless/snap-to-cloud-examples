[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# E20 Example - Interfacing to Adafruit IO

![](https://cloud.githubusercontent.com/assets/1317406/12931178/07558fe8-cf42-11e5-8f7f-f022f0209598.gif)

## Common Setup
Each example in this repo requires some amount of common setup. Please follow the
[common setup instructions](../README.md#common-setup) first.

## Configuring Adafruit IO
To use this example a free Adafruit IO account is required. To sign up, visit:

> https://accounts.adafruit.com/users/sign_up

After signing up, go to your [Adafruit IO settings page](https://io.adafruit.com/settings) and get your AIO API key:

![](https://cloud.githubusercontent.com/assets/1317406/12931309/b10b9b5e-cf42-11e5-84b0-901e029b340a.png)

## Setup Gateway
Simply power up the E20 and load the software onto the E20 (put it in the snap user directory).
You must edit the provided `adafruitio/settings.py` file to use your personal AIO key:

```python
# TODO - Update ADAFRUIT_IO_KEY with your personal Adafruit IO API key
ADAFRUIT_IO_KEY = "ab37939a9873db7e9f97b97a7ed99cb98d98e98baf98be98ad"
```

This example also uses several 3rd-party Python libraries. Install them onto your E20 using

```bash
sudo pip2.7.9 install -r adafruitio/requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/
```

Once both of these steps have been competed, execute the adafruit_example.py Python script as sudo.  

```bash
sudo python2.7.9 adafruit_example.py
```

Now that Adafruit IO and the E20 have been configured, 
the [Feeds page](https://io.adafruit.com/feeds) should new values that were transmitted by the SNAP node.

Now take some time to explore Adafruit IO by creating your own dashboards.
