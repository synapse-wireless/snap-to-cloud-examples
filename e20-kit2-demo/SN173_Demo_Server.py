# Copyright (C) 2015 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse")
# to you to freely modify, redistribute or include this code in any program. The purpose of this code is to help you 
# understand and learn about SNAP by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. 
# If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED,
# INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR
# PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. 
# SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR)
# ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU,
# OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR 
# ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES
# AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.
"""Main file for E20-Kit2-Demo"""

# --------------------------------------------------------------------------------------------------------
# Imports and setup
# --------------------------------------------------------------------------------------------------------
# import basic needs
import logging
import time
import os
import sys
import os.path
import uuid

# import the tornado required components for ioloop and running a small built in web server
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
# Monkey Patch so APY is happy with stock Tornado
tornado.ioloop.IOLoop.timefunc = time.time

# Monkey Patch so Tornado does NOT autoreload the python modules in debug mode,
# because it messes up snapconnect, and we really just want JS/Template reloads.
import tornado.autoreload
tornado.autoreload.start = lambda x=None, y=None: (x,y)

# Tornado options note: Set --logging=none to see all Tornado logging messages
from tornado.options import define, options

# set the tornado web server port
define("port", default=80, help="run on the given port", type=int)

# import the required snap components
from snapconnect import snap
from apy import ioloop_scheduler
# --------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------
# define constants
# --------------------------------------------------------------------------------------------------------
# Enter the address for the target SN173 board here:
SN173_Addr = "\x06\x27\x01"    

log = logging.getLogger('SN173DemoServer')

# Local system settings for E20 environment
serial_conn = snap.SERIAL_TYPE_RS232
serial_port = '/dev/snap1'
snap_addr = None   # Intrinsic address on E20

# If you are using an E10 these are your settings, uncomment these and comment out those in the E20 section.
# Local system settings for E10 environment
# serial_conn = snap.SERIAL_TYPE_RS232
# serial_port = '/dev/ttyS1'
# snap_addr = None   # Intrinsic address on E10

# --------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------
# Class Defitions
# --------------------------------------------------------------------------------------------------------
""" Below are details for the web server portion and would be best explained by
    the tornado documenation web site.
    http://tornado.readthedocs.org/en/latest/index.html
"""
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", tornado.web.RedirectHandler, {"url": "/index.html"}),
            (r"/wshub", WebSocketHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
        ]        
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=None,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    ''' Send and receive websocket messages between server and browser(s).
        Messages TO the browser are encoded "rpc-like" as
            {'kind' : 'funcName', 'args' : params}
        Messages FROM the browser are translated to RPC calls and invoked on
        our SNAP Connect instance.
    '''
    waiters = set()    # Browser connections

    def allow_draft76(self):
        '''Allow older browser websocket versions'''
        return True
    
    def open(self):
        WebSocketHandler.waiters.add(self)

    def on_close(self):
        WebSocketHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, message):
        #log.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(message)
            except:
                log.error("Error sending message", exc_info=True)

    def on_message(self, message):
        '''Translate browser message into RPC function call (into local SnapCom object)'''
        log.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        print "received: ", parsed
        try:
            func = getattr(snapCom, parsed['funcname'])
        except AttributeError:
            log.exception('Browser called unknown function: %s' % str(parsed))
        else:
            try:
                func(*parsed['args'])
            except:
                log.exception('Error calling function: %s' % str(parsed))
            
class SnapCom(object):

    SNAPCONNECT_POLL_INTERVAL = 5 # ms

    def __init__(self):
        self.snapRpcFuncs = {'updateLEDs' : self.updateLEDs,
                            'powerOn173' : self.powerOn173}

        cur_dir = os.path.dirname(__file__)

        # Create SNAP Connect instance. Note: we are using TornadoWeb's scheduler.
        self.snapconnect = snap.Snap(license_file = os.path.join(cur_dir, 'license.dat'),
                                     addr = snap_addr,
                                     scheduler=ioloop_scheduler.IOLoopScheduler(),
                                     funcs = self.snapRpcFuncs
                                    )

        # Connect to local SNAP wireless network
        self.snapconnect.open_serial(serial_conn, serial_port)
        
        # Tell the Tornado scheduler to call SNAP Connect's internal poll function. Tornado already polls asyncore.
        tornado.ioloop.PeriodicCallback(self.snapconnect.poll_internals, self.SNAPCONNECT_POLL_INTERVAL).start()


    '''INCOMING FUNCTION CALLS FROM SNAP NODE(S) TO CLIENT-SIDE JAVASCRIPT'''
    def updateLEDs(self, LED1status, LED2status, LED3status, LED4status):
        '''RPC received from remote module'''
        message = {'kind' : 'updateLEDs', 'args' : [LED1status, LED2status, LED3status, LED4status, True]}
        WebSocketHandler.send_updates(message)  

    def powerOn173(self, pwrStatus):
        '''RPC received from remote module'''
        message = {'kind' : 'powerStatus', 'args' : [pwrStatus]}
        WebSocketHandler.send_updates(message)
        
    '''OUTGOING FUNCTION CALLS TO SNAP NODE(S) FROM CLIENT-SIDE JAVASCRIPT'''
    def buttonS1pressed(self):
        '''Javascript-RPC received from Browser'''
        self.snapconnect.rpc(SN173_Addr, 'buttonS1pressed') 

    def buttonS2pressed(self):
        '''Javascript-RPC received from Browser'''
        self.snapconnect.rpc(SN173_Addr, 'buttonS2pressed')

    def buttonS3pressed(self):
        '''Javascript-RPC received from Browser'''
        self.snapconnect.rpc(SN173_Addr, 'buttonS3pressed')

    def buttonS4pressed(self):
        '''Javascript-RPC received from Browser'''
        self.snapconnect.rpc(SN173_Addr, 'buttonS4pressed') 

    def reset_pressed(self):
        '''Javascript-RPC received from Browser'''
        self.snapconnect.rpc(SN173_Addr, 'reset_pressed')
        
# --------------------------------------------------------------------------------------------------------        

# --------------------------------------------------------------------------------------------------------
# Main start of program
# --------------------------------------------------------------------------------------------------------
def main():

    # create a default logger for all our log data.
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)-8s %(name)-8s %(message)s')
    
    # set the logging to info so we have a fair amount of data that we can see
    log.setLevel(logging.INFO)
    
    # log our beginning
    log.info("***** Begin Console Log *****")

    # set up the web server according to our configuration
    global webApp
    
    tornado.options.parse_command_line()
    tornado.options.logging = logging.DEBUG
    webApp = Application()
    webApp.listen(options.port)
    
    # Create our instance of SNAPconnect for communicating with our SNAP network
    global snapCom
    snapCom = SnapCom()
    
    tornado.ioloop.IOLoop.instance().start()  # call to this method will only return when the process is stopped
        
if __name__ == '__main__':
    main()

# --------------------------------------------------------------------------------------------------------