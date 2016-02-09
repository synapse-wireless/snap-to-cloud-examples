from Adafruit_IO import *
from settings import ADAFRUIT_IO_KEY

from time import sleep


class AdafruitConnector(object):
    def __init__(self):
        # Create an instance of the Adafruit IO REST client.
        self.aio = Client(ADAFRUIT_IO_KEY)

    def publish(self, thing_id, state):
        """Publish a message to Adafruit IO REST API.

        :param str thing_id: The 6-character SNAP MAC Address
        :param dict state: A dictionary containing the new state values for a thing
        """
        print "Status update: ", thing_id
        self.aio.send(thing_id + '-batt', int(state['batt']))
        sleep(1)  # Pause for a second so we don't hit the API throttle limits
        self.aio.send(thing_id + '-state', int(state['button_state']))
        sleep(1)  # Pause for a second so we don't hit the API throttle limits
        self.aio.send(thing_id + '-count', state['button_count'])
