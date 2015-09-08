// (c) Copyright 2015, Synapse Wireless, Inc.

// Send a message over our WebSocket to SNAP Connect server
function send_message(funcname, args)  {
    var message = {funcname:funcname, args:args};
    wsHub.socket.send(JSON.stringify(message));
}

function mcastRpc(group, ttl, func, args) {
    send_message('snap_method', ['mcastRpc', group, ttl, func].concat(args));
}

// WebSocket Hub: Establish a socket between browser and SNAP Connect Web server. Provide API to send/receive messages
var wsHub = {
    socket: null,

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
			try {
				// Execute global function by stringname
				window[message.funcname].apply(window, message.args);
			} catch (err) {
				console.log("Error executing websocket message: " + err.message);
			}
        }
    },
};



// wsHub Callback: Debug log function - TEST
function do_print(message)  {
    console.log(message);
}


