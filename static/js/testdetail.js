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
      case REPORT:
        toReport(msg);
        break;
      case CLOSE:
        console.log(msg);
        alert(msg);
        break;
        //alert(msg);
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

function toReport(msg){
  setting = msg["setting"]
  data = msg["data"]
  tbody = document.createElement("tbody")
  row = document.createElement("tr");
  for (var i in setting) {
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
