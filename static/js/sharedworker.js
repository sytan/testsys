var websocket = null;

const WEBSOCKET = "websocket";
const CLOSE = "close";

var ports = new Array();
onconnect = function(e) {
  var port = e.ports[0];
  ports.push(port);

  port.onmessage = function(e) {

    cmd = e.data.cmd;
    msg = e.data.msg;
    catalog = e.data.catalog;

    if (catalog == WEBSOCKET) {
      data = JSON.stringify(e.data);
      websocket.send(data);
    }else{
      switch (cmd) {
        case SHELL:

          break;
        default:

      }
    }
  }

  if(websocket == null) {
    var wsServer = 'ws://'+location.host+'/ws';
    websocket = new WebSocket(wsServer);

    websocket.onopen = function(evt) {

    }
    websocket.onclose = function(evt) {
      websocket = null;
      data = new Object();
      data.cmd = CLOSE;
      data.msg = "Connection closed by host!";
      data.catalog = WEBSOCKET;
      broadcast(JSON.stringify(data), ports);
    }
    websocket.onmessage = function(evt) {
      broadcast(evt.data, ports);
    }
  }
}

function broadcast(data, ports) {
  for (var i in ports) {
    port = ports[i];
    port.postMessage(data)
  }
}
