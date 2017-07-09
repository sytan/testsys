var conn;

const SHELL = "shell";
const REPORT = "report"

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
    onCommand(exChangeData);
  }
  // Shared worker
  if (typeof(window.SharedWorker) == "undefined") {
    throw("your browser does not support SharedWorkers")
  }
  var worker = new SharedWorker("sharedworker.js");
  worker.port.onmessage = function(event) {
    conole.log(event.data);
  }
  worker.onerror = function(err) {
    console.log(err.message);
    worker.port.close();
  }
};

function onCommand(exChangeData){
  var cmd = exChangeData.cmd
  var msg = exChangeData.msg
  switch (cmd) {
    case SHELL:
      toShell(msg);
      break;
    case REPORT:
      console.log(msg)
      toReport(msg)
      break;
    default:

  }
}

function toShell(msg){
  var output = document.getElementById("output");
  output.appendChild(document.createTextNode(msg+'\n'));
  output.scrollTop = output.scrollHeight;
};
function toReport(msg){
  setting = msg["setting"]
  data = msg["data"]
  tbody = document.createElement("tbody")
  row = document.createElement("tr");
  for (var i in setting) {
    console.log(setting[i]["data"])
    key = setting[i]["data"]
    td = document.createElement("td");
    td.appendChild(document.createTextNode(data[key]));
    row.appendChild(td);
  }

  var table = document.getElementById("testlist")
  tbody.append(row)
  table.append(tbody)
  var num = table.rows.length;
  var pageSize = 10;
  var startRow = (num > pageSize)?num-pageSize:0;
  var endRow = num


  for(var i=1; i<num; i++){
    var row = table.rows[i];
    if(i>=startRow&&i<endRow){
      row.style.display = "table-row";
    }else{
      row.style.display = "none";
    }
  }

}

function toJson(data) {
  var dataJson = data;
  while (typeof(dataJson) != "object"){
     dataJson = JSON.parse(dataJson);
  }
  return dataJson
};

function onOpen() {
  var exChangeData = new Object();
  exChangeData.cmd = "cmd";
  var exChangeJSON = JSON.stringify(exChangeData);
  conn.send(exChangeJSON);
  console.log(exChangeJSON);
};

function onClickSubmit() {
  console.log("i'm submit");
  var exChangeData = new Object();
  var input = document.getElementById("input");
  exChangeData.cmd = "cmd";
  exChangeData.msg = input.value;
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
