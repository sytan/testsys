const SHELL = "shell";
const REPORT = "report"
const WEBSOCKET = "websocket";
const CLOSE = "close";
// Shared worker
if(window.SharedWorker){
  var worker = new SharedWorker("static/js/sharedworker.js");
  worker.port.onmessage = function(e) {
    var data = toJson(e.data);
    onMessage(data);
  }
}else{
  alert("Your browser doesn't support shared worker!");
}

function onMessage(data){

  var cmd = data.cmd;
  var msg = data.msg;
  var catalog = data.catalog;
  if (catalog == WEBSOCKET) {
    switch (cmd) {
      case SHELL:
        toShell(msg);
        break;
      case CLOSE:
        document.getElementById("input").value = msg;
        break;
      default:
    }
  }else{
    switch (cmd) {
      case SHELL:

        break;
      default:
        console.log(data);
    }
  }
}

function toShell(msg){
  var output = document.getElementById("output");
  output.appendChild(document.createTextNode(msg+'\n'));
  output.scrollTop = output.scrollHeight;
};

function onClickSubmit() {
  var data = new Object();
  var input = document.getElementById("input");
  data.cmd = SHELL;
  data.msg = input.value;
  data.catalog = WEBSOCKET;

  console.log("submit :",data);
  //var exChangeJson = JSON.stringify(exChangeData);
  console.log("i'm sending");
  worker.port.postMessage(data);
}

function onEnter(evt) {
  if(evt.keyCode == 13) {
    onClickSubmit()
  }
};

function toJson(data) {
  var dataJson = data;
  while (typeof(dataJson) != "object"){
     dataJson = JSON.parse(dataJson);
  }
  return dataJson
};
