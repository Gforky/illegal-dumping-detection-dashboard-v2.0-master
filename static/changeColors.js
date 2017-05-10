$(document).ready(function() {
	//set some initial styles of buttons
	var blue = "#0055A2";
	//document.getElementsByClassName("dataViews")[0].style.display = "none";
	$('.sysOpsButton').toggleClass('chosenColor');
	//$('.cpuUsage').toggleClass('chosenColor');
	$('.imgStorage').toggleClass('chosenColor');
	$('.AP').toggleClass('chosenColor');
	// js to change Supervision buttons' colors
	$('.findSofa').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findMattress').toggleClass('chosenColor', false);
	  	$('.findFridge').toggleClass('chosenColor', false);
	  	$('.findChair').toggleClass('chosenColor', false);
	  	$('.findTvMonitor').toggleClass('chosenColor', false);
	  	$('.findShoppingCart').toggleClass('chosenColor', false);
	  	$('.findCleanStreet').toggleClass('chosenColor', false);
	})
	$('.findMattress').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findSofa').toggleClass('chosenColor', false);
	  	$('.findFridge').toggleClass('chosenColor', false);
	  	$('.findChair').toggleClass('chosenColor', false);
	  	$('.findTvMonitor').toggleClass('chosenColor', false);
	  	$('.findShoppingCart').toggleClass('chosenColor', false);
	  	$('.findCleanStreet').toggleClass('chosenColor', false);
	})
	$('.findFridge').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findMattress').toggleClass('chosenColor', false);
	  	$('.findSofa').toggleClass('chosenColor', false);
	  	$('.findChair').toggleClass('chosenColor', false);
	  	$('.findTvMonitor').toggleClass('chosenColor', false);
	  	$('.findShoppingCart').toggleClass('chosenColor', false);
	  	$('.findCleanStreet').toggleClass('chosenColor', false);
	})
	$('.findChair').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findMattress').toggleClass('chosenColor', false);
	  	$('.findFridge').toggleClass('chosenColor', false);
	  	$('.findSofa').toggleClass('chosenColor', false);
	  	$('.findTvMonitor').toggleClass('chosenColor', false);
	  	$('.findShoppingCart').toggleClass('chosenColor', false);
	  	$('.findCleanStreet').toggleClass('chosenColor', false);
	})
	$('.findTvMonitor').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findMattress').toggleClass('chosenColor', false);
	  	$('.findFridge').toggleClass('chosenColor', false);
	  	$('.findChair').toggleClass('chosenColor', false);
	  	$('.findSofa').toggleClass('chosenColor', false);
	  	$('.findShoppingCart').toggleClass('chosenColor', false);
	  	$('.findCleanStreet').toggleClass('chosenColor', false);
	})
	$('.findShoppingCart').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findMattress').toggleClass('chosenColor', false);
	  	$('.findFridge').toggleClass('chosenColor', false);
	  	$('.findChair').toggleClass('chosenColor', false);
	  	$('.findTvMonitor').toggleClass('chosenColor', false);
	  	$('.findSofa').toggleClass('chosenColor', false);
	  	$('.findCleanStreet').toggleClass('chosenColor', false);
	})
	$('.findCleanStreet').click(function() {
	  	$(this).toggleClass('chosenColor');
	  	$('.findMattress').toggleClass('chosenColor', false);
	  	$('.findFridge').toggleClass('chosenColor', false);
	  	$('.findChair').toggleClass('chosenColor', false);
	  	$('.findTvMonitor').toggleClass('chosenColor', false);
	  	$('.findShoppingCart').toggleClass('chosenColor', false);
	  	$('.findSofa').toggleClass('chosenColor', false);
	})

	$('.deleteImg').click(function() {
		$('.findSofa').toggleClass('chosenColor', false);
		$('.findMattress').toggleClass('chosenColor', false);
		$('.findFridge').toggleClass('chosenColor', false);
		$('.findChair').toggleClass('chosenColor', false);
		$('.findTvMonitor').toggleClass('chosenColor', false);
		$('.findShoppingCart').toggleClass('chosenColor', false);
		$('.findCleanStreet').toggleClass('chosenColor', false);
	})
})