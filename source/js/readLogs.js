// js functions to dynamically read logs from back-end
$(document).ready(function monitorTraining() {
  var atBottom = 1;
  var testNum = 0;
  $(".trainingLogRefresh").click(function() {
    for(i = 0; i < 10; ++i)
    $("p.trainingLog").append("This is a training output" + i + "<br />")
  })
  $(".trainingLogReset").click(function() {
    $("p.trainingLog").replaceWith("<p class='trainingLog'></p>")
  })

  $(".detectionLogRefresh").click(function() {
    for(i = 0; i < 10; ++i)
    $("p.detectionLog").append("This is a detection output" + i + "<br />")
  })
  $(".detectionLogReset").click(function() {
    $("p.detectionLog").replaceWith("<p class='detectionLog'></p>")
  })

  // check if divs are scrolled to bottom
  $(".train").scroll(function() {
    if(($(this)[0].scrollTop + $(".train").height()) >= $(this)[0].scrollHeight) {
      atBottom = 1;
    } else {
      atBottom = 0;
    }
  })
  // this function will repeatedly check the updates of logs
  var checker = function() {
    testNum++;
    $("p.trainingLog").append("This is a training output " + testNum +  "<br />")
    $("p.detectionLog").append("This is a detection output " + testNum +  "<br />")
    // jquery function to automatically scroll down to bottom of div
    if(atBottom === 1) {
      $(".train").scrollTop($(".train")[0].scrollHeight)
    }    $(".detection").scrollTop($(".detection")[0].scrollHeight)
    //clearInternal(timer)
  }
  timer = setInterval(checker, 500)
})