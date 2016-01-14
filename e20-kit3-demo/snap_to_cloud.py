import os
import sys
import binascii

from snapconnect import snap
from apy import ioloop_scheduler

import tornado.ioloop

if sys.platform == "linux2":
    # E20 built-in bridge
    serial_conn = snap.SERIAL_TYPE_RS232
    serial_port = '/dev/snap1'
    snap_addr = None  # Intrinsic address on Exx gateways
    snap_license = None
elif sys.platform == "Darwin":
    # SS200 USB stick on Mac
    serial_conn = snap.SERIAL_TYPE_SNAPSTICK200
    serial_port = '/dev/snap1'
    snap_addr = None  # Intrinsic address on Exx gateways
    snap_license = None
else:
    # SS200 USB stick on Windows
    serial_conn = snap.SERIAL_TYPE_SNAPSTICK200
    serial_port = 0
    snap_addr = '\x00\x00\x20'  # SNAP Connect address from included License.dat
    # TODO - Probably need to do something with these paths for windows
    cur_path = os.path.normpath(os.path.dirname(__file__))
    snap_license = os.path.join(cur_path, 'License.dat')


class SNAPToCloudExample(object):

    def __init__(self, cloud_connector, poll_interval=10):
        """Initializes an instance of SNAPToCloudExample.
        
        :param cloud_connector: A connection that can publish to a cloud service
        :param int poll_interval: How often SNAPConnect should poll, in milliseconds
        """
        self.cloud_connector = cloud_connector
        snap_rpc_funcs = {'status': self._on_status}

        # Create SNAP Connect instance. Note: we are using Tornado's scheduler.
        self.snapconnect = snap.Snap(
            license_file=snap_license,
            addr=snap_addr,
            scheduler=ioloop_scheduler.IOLoopScheduler(),
            funcs=snap_rpc_funcs)

        self.snapconnect.open_serial(serial_conn, serial_port)

        # Tell tornado to call SNAP connect internals periodically
        tornado.ioloop.PeriodicCallback(self.snapconnect.poll_internals,
                                        poll_interval).start()

        # Start the IOLoop, nothing can happen after this point
        tornado.ioloop.IOLoop.instance().start()

    def _on_status(self, batt, button_state, button_count):
        """Publish status to the cloud."""
        remote_addr = binascii.hexlify(self.snapconnect.rpc_source_addr())
        print batt, button_state, button_count

        self.cloud_connector.publish(remote_addr, {
            "batt": batt,
            "button_state": button_state,
            "button_count": button_count
        })
