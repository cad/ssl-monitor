var canvas;
var ctx;
var x = 1200;
var y = 8000;
var dx = 2;
var dy = 4;
var WIDTH = 800;
var HEIGHT = 600; 
function circle(x,y,r, str, color) {
    drawTextAlongArc(ctx, str, x, y, r + 1, Math.PI)
    ctx.beginPath();
    ctx.arc(x, y, r+2, 0, Math.PI /3, true);
    if (color == "robots_blue"){
	
	ctx.fillStyle="#3300CC";
    } else {
	ctx.fillStyle="#FFFF00";
    }
    ctx.closePath();
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(x,y,r+5,Math.PI, 2*Math.PI, true);
    ctx.strokeStyle="#666666";
    ctx.lineWidth=3;
    ctx.stroke()
    ctx.closePath();
}


function ball(x,y){
    ctx.beginPath();
    ctx.arc(x,y,3,0, Math.PI * 2, true);
    ctx.fillStyle="orange";
    ctx.closePath();
    ctx.fill()
}

function rect(x,y,w,h) {
    ctx.beginPath();
    ctx.rect(x,y,w,h);
    ctx.closePath();
    ctx.fillStyle="#66CC00";
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(400, 300, 66, 0, Math.PI*2, true);
    ctx.lineWidth=5;
    ctx.strokeStyle="#ffffff";
    ctx.stroke();
    ctx.closePath();
    
    ctx.beginPath();
    ctx.moveTo(400,0);
    ctx.lineTo(400,600);
    ctx.strokeStyle="#ffffff";
    ctx.lineWidth=5;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, 300, 90, 0, Math.PI*2, true);
    ctx.lineWidth=5;
    ctx.strokeStyle="#ffffff";
    ctx.stroke();
    ctx.closePath();
    
    ctx.beginPath();
    ctx.arc(800, 300, 90, 0, Math.PI*2, true);
    ctx.lineWidth=5;
    ctx.strokeStyle="#ffffff";
    ctx.stroke();
    ctx.closePath();

}


function clear() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
}

function init() {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    return true;
}

function drawTextAlongArc(context, str, centerX, centerY, radius, angle){
    context.save();
    context.translate(centerX, centerY);
    context.rotate(-1 * angle / 2);
    context.rotate(-1 * (angle / str.length) / 2);
    for (var n = 0; n < str.length; n++) {
        context.rotate(angle / str.length);
        context.save();
        context.translate(0, -1 * radius);
        var char = str[n];
        context.fillText(char, 0, 0);
	context.lineWidth=5;
        context.restore();
    }
    context.restore();
}


function draw(obj) {
    clear();
    ctx.fillStyle = "#FAF7F8";
    rect(0,0,WIDTH,HEIGHT);
    var blues = obj["robots_blue"]
    var yellows = obj["robots_yellow"]
    var balls = obj["balls"] 
    
    for (var k in obj){
	console.log(k);
	
	for (var i in obj[k]) {
	    console.log(i); 
	    ctx.fillStyle = "#444444";
	    if (k == "balls"){
		ball(obj[k][i][0], obj[k][i][1])
	    } else {
		circle(obj[k][i][0], obj[k][i][1], 10, i,k);
	    }
	}    
    }
}
    
$(function() {
    init()
    if ("WebSocket" in window) {
	var prot;

	if(document.domain == "127.0.0.1"){
	    prot = "ws";
	} else {
	    prot = "ws";
	}
//	alert(prot);
        ws = new WebSocket(prot + "://" + document.domain + ":8000/websocket");
        ws.onmessage = function (msg) {
            
	    console.log("WS:" + msg.data);
	    var obj = jQuery.parseJSON(msg.data);
	    draw(obj);
	    ws.send("true");
        };
    };


    window.onbeforeunload = function() {
        ws.onclose = function () {};
        ws.close()
    };
});

