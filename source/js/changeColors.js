$(document).ready(function() {
	//set some initial styles of buttons
	var blue = "#0055A2";
	document.getElementsByClassName("dataViews")[0].style.display = "none";
	document.getElementsByClassName("sysOpsButton")[0].style.backgroundColor = blue;
	document.getElementsByClassName("cpuUsage")[0].style.backgroundColor = blue;
	document.getElementsByClassName("imgStorage")[0].style.backgroundColor = blue;
	document.getElementsByClassName("AP")[0].style.backgroundColor = blue;
	document.getElementsByClassName("completedTasks")[0].style.backgroundColor = blue;
	// js to change Supervision buttons' colors
	$('.findSofa').click(function() {
	  	$(this).toggleClass('chosenColor');
	})
	$('.findMattress').click(function() {
	  	$(this).toggleClass('chosenColor');
	})
	$('.findTvMonitor').click(function() {
	  	$(this).toggleClass('chosenColor');
	})

	$('.deleteImg').click(function() {
		$('.findSofa').toggleClass('chosenColor', false);
		$('.findMattress').toggleClass('chosenColor', false);
		$('.findTvMonitor').toggleClass('chosenColor', false);
	})
})