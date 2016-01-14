import os
import sys
import json
import binascii

from snapconnect import snap
from apy import ioloop_scheduler

import tornado.ioloop
from tornado import httpclient

from pyonep import onep  # Exosite Python Library


# TODO: Replace these with values from your own Exosite account and resource
# We want to map SN171 SNAP addresses to Exosite CIKs
EXOSITE_CIKS = {"XXXXXX": 'unique Exosite CIK here',
                "YYYYYY": 'another unique Exosite CIK here'}

SNAPCONNECT_POLL_INTERVAL = 10  # milliseconds

if sys.platform == "linux2":
    # E20 built-in bridge
    serial_conn = snap.SERIAL_TYPE_RS232
    serial_port = '/dev/snap1'
    snap_addr = None  # Intrinsic address on Exx gateways
    snap_license = None
else:
    # SS200 USB stick on Windows
    serial_conn = snap.SERIAL_TYPE_SNAPSTICK200
    serial_port = 0
    snap_addr = '\x00\x00\x20'  # SNAP Connect address from included License.dat
    cur_path = os.path.normpath(os.path.dirname(__file__))
    snap_license = os.path.join(cur_path, 'License.dat')


class ExositeExample(object):
    def __init__(self):
        """
        Initializes an instance of ExositeExample
        :return:
        """
        snap_rpc_funcs = {'status': self._on_status}

        # Create SNAP Connect instance. Note: we are using Tornado's scheduler.
        self.snapconnect = snap.Snap(
            license_file=snap_license,
            addr=snap_addr,
            scheduler=ioloop_scheduler.IOLoopScheduler(),
            funcs=snap_rpc_funcs
        )

        self.snapconnect.open_serial(serial_conn, serial_port)

        # Tell tornado to call SNAP connect internals periodically
        tornado.ioloop.PeriodicCallback(self.snapconnect.poll_internals, SNAPCONNECT_POLL_INTERVAL).start()

        self.exosite = onep.OnepV1()

    def _on_status(self, batt, button_state, button_count):
        """
        Writes the various status values received from a node to Exosite
        :return: None
        """
        remote_addr = binascii.hexlify(self.snapconnect.rpc_source_addr())
        print batt, button_state, button_count

        # Use the Exosite Python Library to format the message
        jsonreq = {"auth": {"cik": EXOSITE_CIKS[remote_addr]},
                   "calls": self.exosite._composeCalls([('writegroup', [[[{"alias": "batt"}, int(batt)],
                                                                         [{"alias": "state"}, int(button_state)],
                                                                         [{"alias": "count"}, button_count]]])])}
        # Create a Tornado HTTPRequest
        request = httpclient.HTTPRequest(url=self.exosite.onephttp.host + self.exosite.url,
                                         method='POST',
                                         headers=self.exosite.headers,
                                         body=json.dumps(jsonreq))

        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(request, self._handle_request)

    @staticmethod
    def _handle_request(response):
        """
        Prints the response of a HTTPRequest
        :param response: HTTPRequest
        :return:
        """
        if response.error:
            print "Error:", response.error
        else:
            print response.body


def main():
    example = ExositeExample()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
