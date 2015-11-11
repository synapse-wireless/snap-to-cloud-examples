/*
 Copyright (C) 2015 Synapse Wireless, Inc.
 Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse")
 to you to freely modify, redistribute or include this code in any program. The purpose of this code is to help you 
 understand and learn about SNAP by code examples.
 BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. 
 If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this code.
 THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED,
 INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR
 PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. 
 SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR)
 ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU,
 OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR 
 ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES
 AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.
 */

// Main javascript file for SN173 Demo Web Interface
// This version uses jQuery, and Websockets
               
// Document Loaded callback
$(document).ready(function() {
    wsHub.start();  
    wsHub.register('updateLEDs', updateLEDs);  
    wsHub.register('powerStatus', powerStatus); 
});

function ButtonS1() {
  //$("#LED1").toggle();
  sendRpc("buttonS1pressed", [])
}

function ButtonS2() {
  //$("#LED2").toggle();
  sendRpc("buttonS2pressed", [])
}

function ButtonS3() {
  //$("#LED3").toggle();
  sendRpc("buttonS3pressed", [])
}

function ButtonS4() {
  //$("#LED4").toggle();
  sendRpc("buttonS4pressed", [])
}

function ButtonReset() {
  //$("#LED4").toggle();
  sendRpc("reset_pressed", [])
}

function updateLEDs(LEDmsg) {
  //args[0] = LED1 Status
  //args[1] = LED2 Status
  //args[2] = LED3 Status
  //args[3] = LED4 Status
  //args[4] = PWR LED Status
  if (LEDmsg.args[0]) {
    $("#LED1").show();
  } else {
    $("#LED1").hide();
  };

  if (LEDmsg.args[1]) {
    $("#LED2").show();
  } else {
    $("#LED2").hide();
  };

  if (LEDmsg.args[2]) {
    $("#LED3").show();
  } else {
    $("#LED3").hide();
  };

  if (LEDmsg.args[3]) {
    $("#LED4").show();
  } else {
    $("#LED4").hide();
  };

  if (LEDmsg.args[4]) {
    $("#LEDPWR").show();
  } else {
    $("#LEDPWR").hide();
  };
}

function powerStatus(pwrStatus) {
  if (pwrStatus.args[0]) {
    $("#LEDPWR").show();
  } else {
    $("#LED1").hide();
    $("#LED2").hide();
    $("#LED3").hide();
    $("#LED4").hide();
    $("#LEDPWR").hide();
  };
}

function socketClosed() {
  $("#LED1").hide();
  $("#LED2").hide();
  $("#LED3").hide();
  $("#LED4").hide();
  $("#LEDPWR").hide();
}

// Send an RPC over Websocket
function sendRpc(funcname, args)  {
    var message = {funcname:funcname, args:args};
    wsHub.socket.send(JSON.stringify(message));
}

// WebSocket Hub: Establish a socket between browser and server. Provide API to send/receive messages
var wsHub = {
    socket: null,
    registry: new Array(),

    register: function(kind, callback)  {
        wsHub.registry.push( {kind:kind, callback:callback} );
    },

    start: function() {
        var host = "ws://" + location.host + "/wshub"

        // Detect WebSocket support
        if ("WebSocket" in window) {
            // Modern browsers
            wsHub.socket = new WebSocket(host);
        } else if ("MozWebSocket" in window) {
            // Firefox 6
            wsHub.socket = new MozWebSocket(host);
        }
        else  {
            $('body').html("<h1>Error</h1><p>Your browser does not support HTML5 Web Sockets.</p>");
            return;
        }
    
        wsHub.socket.onmessage = function(event) {
            message = JSON.parse(event.data);
            var i = 0;
            for (i = 0; i < wsHub.registry.length; i++)  {
                var observer = wsHub.registry[i];
                if (observer.kind === message.kind)  {
                    observer.callback(message);
                }
            }
        },

        wsHub.socket.onclose = function() {
            socketClosed();
        }
    },
};