// js functions to dynamically read logs from back-end
$(document).ready(function monitorTraining() {
  $(".trainingLogRefresh").click(function() {
    for(i = 0; i < 10; ++i)
    $("p.trainingLog").append("This is a training output" + i + "<br />")
  })
  $(".trainingLogReset").click(function() {
    $("p.trainingLog").replaceWith("<p class='trainingLog'></p>")
  })

  $(".alertLogRefresh").click(function() {
    for(i = 0; i < 10; ++i)
    $("p.alertLog").append("This is a alert output" + i + "<br />")
  })
  $(".alertLogReset").click(function() {
    $("p.alertLog").replaceWith("<p class='alertLog'></p>")
  })

  $(".detectionLogRefresh").click(function() {
    for(i = 0; i < 10; ++i)
    $("p.detectionLog").append("This is a detection output" + i + "<br />")
  })
  $(".detectionLogReset").click(function() {
    $("p.detectionLog").replaceWith("<p class='detectionLog'></p>")
  })
  // this function will repeatedly check the updates of logs
  var checker = function() {
    $("p.trainingLog").append("This is a training output <br />")
    $("p.alertLog").append("This is a alert output <br />")
    $("p.detectionLog").append("This is a detection output <br />")
    // jquery function to automatically scroll down to bottom of div
    $(".train").scrollTop($(".train")[0].scrollHeight)
    $(".alert").scrollTop($(".alert")[0].scrollHeight)
    $(".detection").scrollTop($(".detection")[0].scrollHeight)
    //clearInternal(timer)
  }
  timer = setInterval(checker, 500)
})