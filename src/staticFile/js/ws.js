const socket = new WebSocket('ws://' + window.location.host + '/websocket');
setInterval(ping, 100)
function ping(){
    socket.send(JSON.stringify({"type": "ping"}));
    }

socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.type

    if (messageType === 'pong'){
        var a = document.getElementById('noti')
        a.hidden = false
    }
}