import json
import os
import boto3
import ssl
import urllib
import paho.mqtt.client as mqtt
from settings import PROFILE_NAME, CAFILE, CERTIFICATE_CERT, CERTIFICATE_KEY

class AWSConnector(object):
    def __init__(self):
        self.session = boto3.session.Session(profile_name=PROFILE_NAME)
        self.iot = self.session.client('iot')
        self.endpoint_address = self.iot.describe_endpoint()['endpointAddress']
        self.client_id = self.endpoint_address.split(".")[0]

        if not os.path.isfile(CAFILE):
            # Get a CA file if we don't have one
            self.get_cafile()
            
        self.mqtt_client = None
        self.setup_mqtt_client()

    def _on_mqtt_log(self, client, userdata, level, buf):
        """Map from Paho MQTT log events to Python logging."""
        print buf

    def setup_mqtt_client(self):
        # Create MQTT client
        self.mqtt_client = mqtt.Client(self.client_id)
        self.mqtt_client.on_log = self._on_mqtt_log

        # Authenticate using TLS mutual authentication with a client certificate
        self.mqtt_client.tls_set(CAFILE, CERTIFICATE_CERT, CERTIFICATE_KEY, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2)

        # 8883 is the default port for MQTT over SSL/TLS
        self.mqtt_client.connect(self.endpoint_address, port=8883)

    def get_cafile(self):
        AUTHORITY_LOCATION = "https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem"

        url = urllib.URLopener()
        url.retrieve(AUTHORITY_LOCATION, CAFILE)
    
    def publish(self, thing_id, state):
        topic = "$aws/things/"+str(thing_id)+"/shadow/update"
        update = json.dumps({"state": {"reported": state}})
        print update
        self.mqtt_client.publish(topic, payload=update, qos=1)