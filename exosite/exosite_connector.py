import json

from pyonep import onep  # Exosite Python Library
from tornado import httpclient

# TODO: Replace these with values from your own Exosite account and resource
# We want to map SN171 SNAP addresses to Exosite CIKs
EXOSITE_CIKS = {"XXXXXX": 'unique Exosite CIK here', "YYYYYY": 'another unique Exosite CIK here'}


class ExositeConnector(object):
    def __init__(self):
        self.exosite = onep.OnepV1()

    def publish(self, thing_id, state):
        """Publish a message to Exosite API.

        :param str thing_id: The 6-character SNAP MAC Address
        :param dict state: A dictionary containing the new state values for a thing
        """
        # Use the Exosite Python Library to format the message
        jsonreq = {"auth": {"cik": EXOSITE_CIKS[thing_id]},
                   "calls": self.exosite._composeCalls([('writegroup', [[[{"alias": "batt"}, int(state[
                       'batt'])], [{"alias": "state"}, int(state['button_state'])], [{"alias": "count"}, state[
                           'button_count']]]])])}
        # Create a Tornado HTTPRequest
        request = httpclient.HTTPRequest(url=self.exosite.onephttp.host + self.exosite.url,
                                         method='POST',
                                         headers=self.exosite.headers,
                                         body=json.dumps(jsonreq))

        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(request, self._handle_request)

    @staticmethod
    def _handle_request(response):
        """Prints the response of a HTTPRequest.

        :param response: HTTPRequest
        :return:
        """
        if response.error:
            print "Error:", response.error
        else:
            print response.body
