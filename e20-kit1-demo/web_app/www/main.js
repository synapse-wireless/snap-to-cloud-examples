// (c) Copyright 2015, Synapse Wireless, Inc.
// Main javascript file for SNAP Demo

// Document Loaded callback
$(document).ready(function() {
    // Initialize websocket connection from browser to E20
    wsHub.start();
});

// Call-in from server SNAP application
// Status update from addressed node. Update table to reflect status.
function report_status(addr, batt, pressed, count) {
    console.log("status: " + addr + ", count=" + count);    

    // If there's not already a table row for this address, append one.
    var row = $('#' + addr)
    if (row.length == 0) {
        // Make a new row
        var inp_cell = '<td><input type="checkbox"/></td>';
        $("#node_table").append('<tr id="' + addr + '"><td>addr</td><td>batt</td><td>pressed</td><td>count</td>' + inp_cell + '</tr>');
        row = $('#' + addr);
        
        // Hook the "Lights" checkbox
        row.find('td:eq(4)').change(function(ev) {
            // Send command to addressed node when changed
            set_lights(addr, ev.target.checked ? 1 : 0);
        });
    }
    
    // Update table with new status
    row.find('td:eq(0)').text(addr);
    row.find('td:eq(1)').text(batt);
    row.find('td:eq(2)').text(pressed);
    row.find('td:eq(3)').text(count);
}

// Call 'lights()' function on E20 -> addressed SNAP node
function set_lights(addr, pattern) {
    send_message('lights', [addr, pattern]);
}
