// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function get_x(x){
    var canvas = document.getElementById('mycanvas');
    let a = canvas.getBoundingClientRect();
    return x-a.left;
}
function get_y(y){
    var canvas = document.getElementById('mycanvas');
    let a = canvas.getBoundingClientRect();
    return y-a.top;
}
function draw(event) {
   
    var y = get_y(event.clientY);
    var x = get_x(event.clientX);
    console.log(x,y)
    canvas = document.getElementById('mycanvas');
    ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#ACD3ED';
    ctx.moveTo(x, y);
    ctx.lineTo(x, y);
    ctx.stroke();

    sendPlayerLocation(x, y);
}
function show_others_draw(x, y) {
    canvas = document.getElementById('mycanvas');
    ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#ACD3ED';
    ctx.moveTo(x, y);
    ctx.lineTo(x, y);
    ctx.stroke();
}
function sendPlayerLocation(x, y) {
    socket.send(JSON.stringify({"type": "PlayerLocation", "x": x, "y": y}));
}
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.type

    switch (messageType) {
        case 'PlayerLocation':
            x = message.x
            y = message.y
            show_others_draw(x, y);
            break;
        case 'pong':
            var a = document.getElementById('noti')
            a.hidden = false
            break;
    }
}
function start() {
    document.addEventListener("mousemove", draw);
}
function stop() {
    document.removeEventListener('mousemove', draw);
}
document.addEventListener("mouseup", stop)
document.addEventListener("mousedown", start)

//document.addEventListener("click", printMousePos);
//document.addEventListener("keydown", function (event) {
//     handleEvent(event, true);
//});