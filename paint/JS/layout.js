"use strict"

// css-tricks.com/snippets/css/a-guide-to-flexbox/
function flex_this () {
	foreach($$("[flexer]"), function (elem) {
		var dir = elem.getAttribute("flexer")
		elem.style["display"] = "flex"
		elem.style["flexFlow"] = dir
	})
	foreach($$("[flex]"), function (elem) {
		var attr = elem.getAttribute("flex")
		elem.style["flex"] = attr
	})

	var align = { start:"flex-start", end:"flex-end", center:"center",
		between:"space-between", around:"space-around", baseline: "baseline" }

	foreach($$("[justify]"), function (elem) {
		var attr = elem.getAttribute("justify")
		elem.style["justifyContent"] = align[attr]
	})
	foreach($$("[align]"), function (elem) {
		var attr = elem.getAttribute("align")
		elem.style["alignItems"] = align[attr]
	})
	foreach($$("[align-self]"), function (elem) {
		var attr = elem.getAttribute("align-self")
		elem.style["alignSelf"] = align[attr]
	})
	foreach($$("[test]"), function (elem) {
		var attr = elem.getAttribute("test")
		elem.style["background"] = attr || "red"
	})
	foreach($$("[paper]"), function (elem) {
		elem.classList.add("paper")
	})
}

function foreach (arr, func) {
	[].forEach.call(arr, func)
}