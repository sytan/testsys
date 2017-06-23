var conn;

window.onload = function () {
  if (!window["WebSocket"]) {
    alert("Your browser does not support websocket!");
    return
  }
  var wsServer = 'ws://'+location.host+'/ws';
  conn = new WebSocket(wsServer);
  conn.onopen = function(evt) {
    onOpen();
  };
  conn.onclose = function (evt) {
    document.getElementById("input").value = "Connection closed!"
  };
  conn.onerror = function(evt) {
    alert("i'm error");
    alert(evt.data);
  };
  conn.onmessage = function(evt) {
    var exChangeData = toJson(evt.data);
    console.log(exChangeData);
    onReadPort(exChangeData.Msg);
  }
};

function onReadPort(msg){
  var output = document.getElementById("output");
  output.appendChild(document.createTextNode(msg+'\n'));
  output.scrollTop = output.scrollHeight;
};

function toJson(data) {
  var dataJson = data;
  while (typeof(dataJson) != "object"){
     dataJson = JSON.parse(dataJson);
  }
  return dataJson
};

function onOpen() {
  var exChangeData = new Object();
  exChangeData.Cmd = "cmd";
  var exChangeJSON = JSON.stringify(exChangeData);
  conn.send(exChangeJSON);
  console.log(exChangeJSON);
};

function onClickSubmit() {
  console.log("i'm submit");
  var exChangeData = new Object();
  var input = document.getElementById("input");
  exChangeData.Cmd = "cmd";
  exChangeData.Msg = input.value;
  console.log("submit :",exChangeData);
  var exChangeJson = JSON.stringify(exChangeData);
  if (!conn) {
    return false;
  }
  console.log("i'm sending");
  conn.send(exChangeJson);
};

function onEnter(evt) {
  if(evt.keyCode == 13) {
    onClickSubmit()
  }
};
