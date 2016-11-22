"use strict"

//****--------------------------------------------------------------------
//USER ID
//****--------------------------------------------------------------------

/*function rand () {
	var array = new Uint32Array(1)
	window.crypto.getRandomValues(array)
	return array[0]
}

function get_user_ID () {
	if(!localStorage.userID)
		localStorage.userID = rand()
	return localStorage.userID
}

var user = "user" + get_user_ID()*/


//****--------------------------------------------------------------------
//WEBSOCKET CONNECTION
//****--------------------------------------------------------------------

var connection // = PL_websocket()
PL.app_channel()
.then(function (ws) {
	connection = ws
})


//****--------------------------------------------------------------------
//CONTENT
//****--------------------------------------------------------------------

var mouse_down = false

document.onmousedown = function() { mouse_down = true }
document.onmouseup = function() { mouse_down = false }
document.ontouchstart = document.onmousedown
document.ontouchend = document.onmouseup

window.onresize = function () {
	create_color_picker()
	create_drawing_canvas()
}


var picked_color = [255,0,0,255]

function create_color_picker () {
	var c = color_picker.getContext("2d")
	var rect = color_picker.getBoundingClientRect()
	color_picker.width = rect.width
	var w = color_picker.width
	var gradient = c.createLinearGradient(0,0,w,0)
	gradient.addColorStop(0/6,"rgb(255,0,0)")
	gradient.addColorStop(1/6,"rgb(255,255,0)")
	gradient.addColorStop(2/6,"rgb(0,255,0)")
	gradient.addColorStop(3/6,"rgb(0,255,255)")
	gradient.addColorStop(4/6,"rgb(0,0,255)")
	gradient.addColorStop(5/6,"rgb(255,0,255)")
	gradient.addColorStop(6/6,"rgb(255,0,0)")
	c.fillStyle = gradient
	c.fillRect(0,0,w,w)


	color_picker.onclick = function(event) {
		var x = event.clientX - rect.left
		var y = event.clientY - rect.top
		// scale
		//x *= w / rect.width
		
		picked_color = c.getImageData(x, y, 1, 1).data
		var R = picked_color[0], G = picked_color[1], B = picked_color[2]
		rgb.style.background = "rgba(" + R + ',' + G + ',' + B + ",1)"
	}

	color_picker.onmousemove = function (e) {
		if(mouse_down)
			color_picker.onclick(e)
	}
	color_picker.ontouchstart = function (e) {
		color_picker.onclick(e.targetTouches[0])
	}
	color_picker.ontouchmove = function (e) {
		color_picker.onmousemove(e.targetTouches[0])
	}
}

function create_drawing_canvas () {
	var c = drawing_canvas.getContext("2d")
	var rect = drawing_canvas.getBoundingClientRect()
	drawing_canvas.width = rect.width
	drawing_canvas.height = rect.height
	var scale = drawing_canvas.width / rect.width
	var start = false
	var data = { event: "draw", x: 0, y: 0 }

	c.lineWidth = 10
	c.lineJoin = "round"
	c.lineCap = "round"

	function coords (event) {
		var x = event.clientX - rect.left
		var y = event.clientY - rect.top
		return {x: x, y: y}
	}
	
	drawing_canvas.onmousedown = function (event) {
		start = coords(event)
	}
	drawing_canvas.onmousemove = function (event) {
		if(!start)
			return
		var move = coords(event)

		var R = picked_color[0], G = picked_color[1], B = picked_color[2]
		c.beginPath()

		c.strokeStyle = "rgba(" + R + ',' + G + ',' + B + ",1)"

		c.moveTo(start.x, start.y)
		c.lineTo(move.x, move.y)
		c.stroke()
		start = move
		data.x = move.x / rect.width, data.y = move.y / rect.height
		var R = picked_color[0], G = picked_color[1], B = picked_color[2]
		data.color = [R,G,B]

		connection.send(JSON.stringify(data))
	}
	drawing_canvas.onmouseup = function (event) {
		start = false
		c.beginPath()
	}

	drawing_canvas.ontouchstart = function (e) {
		e.preventDefault() // prevents chrome from refreshing when painting from top to bottom
		drawing_canvas.onmousedown(e.targetTouches[0])
	}
	drawing_canvas.ontouchmove = function (e) {
		drawing_canvas.onmousemove(e.targetTouches[0])
	}
	drawing_canvas.ontouchend = function (e) {
		drawing_canvas.onmouseup(e.targetTouches[0])
	}

	var clear = JSON.stringify({ event: "clear" })
	drawing_canvas.clear = function () {
		c.clearRect(0, 0, drawing_canvas.width, drawing_canvas.height)
		//console.log(clear)
		connection.send(clear)
	}
}


//****--------------------------------------------------------------------
//ORIENTATION
//****--------------------------------------------------------------------
/*
if (!window.DeviceOrientationEvent)
	console.error("DeviceOrientation is NOT supported")

if (!window.DeviceMotionEvent)
	console.error("DeviceMotionEvent is NOT supported")
window.ondeviceorientation = function (e) { //alpha, beta, gamma
	//var b = document.getElementById("background");
	//b.style.transform = "rotate("+ e.alpha +"deg)";// rotate3d(1,0,0, "+ (beta*-1)+"deg)";
}

window.ondevicemotion = function (e) {
	//console.log(e.acceleration.x);
	visitantdata.attributes[0].value = e.acceleration.x;
	visitantdata.attributes[1].value = e.acceleration.y;
	visitantdata.attributes[2].value = e.acceleration.z;
	visitantdata.attributes[3].value = now();
}*/