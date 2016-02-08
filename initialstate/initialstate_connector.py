import json

from tornado import httpclient

# TODO: Replace these with values from your own Initial State account and buckets
# We want to map Initial State buckets to nodes
INITIAL_STATE_BUCKETS = {"XXXXXX": "unique Initial State bucket key here",
                         "YYYYYY": "another unique Initial State bucket key here"}  # yapf: disable
ACCESS_KEY = "enter unique access key here"
INITIAL_STATE_URL = "https://groker.initialstate.com/api/events"


class InitialStateConnector(object):
    def publish(self, thing_id, state):
        """Publish a message to Initial State API

        :param str thing_id: The 6-character SNAP MAC Address
        :param dict state: A dictionary containing the new state values for a thing
        """

        try:
            headers = {
                "X-IS-AccessKey": ACCESS_KEY,
                "X-IS-BucketKey": INITIAL_STATE_BUCKETS[thing_id],
                "Content-Type": "application/json"
            }
        except KeyError:
            print "Could not find SNAP address %s in INITIAL_STATE_BUCKETS" % thing_id
            return

        jsonreq = [
            {"key": "batt", "value": int(state['batt'])},
            {"key": "state", "value": int(state['button_state'])},
            {"key": "count", "value": state['button_count']}
        ]
        # Create a Tornado HTTPRequest
        request = httpclient.HTTPRequest(url=INITIAL_STATE_URL,
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(jsonreq))

        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(request, self._handle_request)

    @staticmethod
    def _handle_request(response):
        """Prints the response of a HTTPRequest

        :param response: HTTPRequest
        :return:
        """
        if response.error:
            print "Error:", response.error
        else:
            print response.body
