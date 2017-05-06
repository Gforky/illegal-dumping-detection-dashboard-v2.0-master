var app = angular.module('dashboard', ['ngAnimate', 'ngTouch'])

var confirmationList = []
var objectList = ['mattress', 'sofa', 'tvmonitor', 'fridge', 'chair', 'shoppingcart', 'cleanstreet']
for(index = 0; index < objectList.length; ++index) {
  confirmationList.push(false)
}

app.controller('trainCtrl', function($scope) {
// add the function to dynamically display the cnn traning process outputs

})

app.controller('detectCtrl', function($scope) {
// add the function to continously display the detected trash
})

app.controller('chartCtrl', function($scope) {
// add the function to dynamically read the AP data from back-end
})

app.controller('inputCtrl', function($scope) {
// add the function to handle the input data, including images, labels, etc.
})

app.controller('searchCtrl', function($scope) {
$scope.searchButton = function() {
  // add the function for image search
}
})

app.controller('modelCtrl', function($scope) {
// add the function to change the network correspondingly
$scope.VGG16 = function() {
  $scope.networkName='VGG16'
}

$scope.ZF = function() {
  $scope.networkName='ZF'
}

$scope.VGG_CNN_M_1024 = function() {
  $scope.networkName='VGG_CNN_M_1024'
}
})

app.controller('realTimeTrainingCtrl', function($scope) {

})

app.controller('manuallyRetrain', function($scope) {
  $scope.retrain = function() {
    $.ajax({
      url: '/retrain-model',
      type: 'POST',
      success: function(response) {
        console.log($.parseJSON(response))
        // convert JSON object into javascript array
      },
      error: function(error) {
        console.log(error)
      }
    })
  }
})

//app.controller('todoCtrl', ['$scope', '$interval', function($scope, $interval) {
// controller for to-do list of trash collections
//  $scope.tasks = [];
//  $scope.title = 'test';
//  $scope.add = function() {
//    $scope.tasks.push($scope.title);
//  }
//  $scope.delete = function() {
//    $scope.tasks.splice(this.$index, 1);
//  }

//  function updateTodoList() {
//    $scope.tasks.push($scope.title);
//  }

// set interval to continously update the list
//  var updateTime = $interval(updateTodoList, 1000);

//  element.on('$destroy', function() {
//    $interval.cancel(updateTime);
//  })
//}])

app.controller('classifyCtrl', function($scope) {
  var todoCtrl = angular.element(document.getElementById('slider')).scope()

})

app.controller('todoCtrl', function($scope) {
  /*$scope.photos = [
    {src: '/images/tv-monitor/345361872_9e7aff54f5_b.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/501173063_6e1b3775e5_b.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/6197024779_31371d2b4b_b.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/computer-monitor-in-front-of-a-full-skip-or-dumpster-with-unwanted-achk1e.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/16627981590_c605c940ac_b.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/EP-160139853.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/1.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/3.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/8.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/160424-analog-tv-set-recycle-yh-0754a_160bd0ae9c2c95d18a1102fed4884ec3.nbcnews-fp-1200-800.jpg', class: 'tv-monitor', accuracy: '0.82'},
    {src: '/images/tv-monitor/802263183_cb915bcfd3_b.jpg', class: 'tv-monitor', accuracy: '0.82'}
  ];*/
  $scope.photos = [
                    {src: '/images/welcome.jpg', class: 'N/A', accuracy: 'N/A'}                  
                  ];

  // initial image index
  $scope._Index = 0;
  var photo = $scope.photos[0]
  photo.show = true
  $scope.classificationResult = "N/A";
  $scope.accuracy = "N/A";

  // if current image is the same as requested image
  $scope.isActive = function(index) {
    if($scope.photos[$scope._Index]) {
      $scope.classificationResult = $scope.photos[$scope._Index].class;
      $scope.accuracy = $scope.photos[$scope._Index].accuracy;
    } else {
      $scope.classificationResult = "";
      $scope.accuracy = "";
    }
    return $scope._Index === index;
  }
  // show prev image
  $scope.showPrev = function() {
    var original_index = $scope._Index
    $scope._Index = ($scope._Index > 0) ? --$scope._Index : $scope.photos.length - 1;
    $scope.photos[original_index].show = false
    $scope.photos[$scope._Index].show = true
  }
  // show next image
  $scope.showNext = function() {
    var original_index = $scope._Index
    $scope._Index = ($scope._Index < $scope.photos.length - 1) ? ++$scope._Index : 0;
    $scope.photos[original_index].show = false
    $scope.photos[$scope._Index].show = true
  }
  // show a specific image
  $scope.showPhoto = function(index) {
    $scope._Index = index;
  }

  /*$.ajax({
    url: '/trigger_detect',
    type: 'POST',
    success: function(response) {
      //console.log($.parseJSON(response))
      var problem_list = $.parseJSON(response)
      var arr_length = problem_list.length
      for(var i = 0; i < arr_length; ++i) {
        //console.log("iteration: " + i)
        var data = problem_list[i]
        var img_path = data[0]
        var labels = data[1]
        var accuracies = data[2]

        var labels_length = labels.length
        for(var j = 0; j < labels_length; ++j) {
          var temp = labels[j]
          labels[j] = temp.slice(2, -3)
        }

        img_path = img_path.slice(6, )
    
        //console.log(img_path)
        //console.log(labels[0])
        //console.log(accuracies[0])

        var entry = {src: img_path, class: labels[0], accuracy: accuracies[0]}
        $scope.photos.push(entry)
      }

      //$scope._Index = ($scope._Index < $scope.photos.length - 1) ? ++$scope._Index : 0;
      // convert JSON object into javascript array
      console.log($scope._Index)
    },
    error: function(error) {
      console.log(error)
    }
  })*/

  // delete image and shift to next image
  $scope.removePhoto = function() {
      // image labels and the image source info
    $("b.oneTimeClassificationResult").replaceWith("<b class='oneTimeClassificationResult'>Waiting for classification result</b>")
    /*if($scope._Index != 0) {
      console.log($scope._Index)
      if($scope.photos[$scope._Index]) { // check if any images waitting for confirmation
        var labels = []
        for(index = 0; index < objectList.length; ++index) {
          if(confirmationList[index]) {
            labels.push(index)
          }
        }
        var myData =  {
                        'labels' : labels, 
                        'img_path' : $scope.photos[$scope._Index].src
                      }
        $.ajax({
          url: '/imgConfirmation',
          contentType: 'application/json',
          dataType: 'json',
          type: 'POST',
          data: JSON.stringify(myData),
          success: function(response) {
            //console.log($.parseJSON(response))
            // convert JSON object into javascript array
          },
          error: function(error) {
            console.log(error)
          }
        })
        for(index = 0; index < confirmationList.length; ++index) {
          confirmationList[index] = false;
        }
        $scope.photos.splice($scope._Index, 1)
        $scope._Index = 0
        //$scope._Index = ($scope._Index < $scope.photos.length - 1) ? ++$scope._Index : 0
        if($scope.photos.length === 0) {
          $scope.classificationResult = "";
          $scope.accuracy = "";
        }
      }
    }*/
    if($("img.slide").attr("src") != 'static/images/welcome.jpg') { // check if any images waitting for confirmation
        var labels = []
        for(index = 0; index < objectList.length; ++index) {
          if(confirmationList[index]) {
            labels.push(index)
          }
        }
        var myData =  {
                        'labels' : labels, 
                        'img_path' : $("img.slide").attr("src")
                      }
        $.ajax({
          url: '/imgConfirmation',
          contentType: 'application/json',
          dataType: 'text',
          type: 'POST',
          data: JSON.stringify(myData),
          success: function(response) {
            console.log($.parseJSON(response))
            // convert JSON object into javascript array
          },
          error: function(error) {
            console.log(error)
          }
        })
        for(index = 0; index < confirmationList.length; ++index) {
          confirmationList[index] = false;
        }
        $("img.slide").replaceWith("<img class='slide' src='static/images/welcome.jpg'>")
        $("span.classificationResult").replaceWith("<span style='color:#ff4000' class='classificationResult'>N/A</span>")
        $("span.accuracy").replaceWith("<span style='color:#ff4000' class='accuracy'>N/A</span>")
      }
  }
  // refresh the image list in the slider
  $scope.refreshConfirmationImageList = function() {
    var threshold = $("input.accuracyThreshold").val() / 100
    var myData = { 'threshold' : threshold}
    $("b.oneTimeClassificationResult").replaceWith("<b class='oneTimeClassificationResult'>Waiting for classification result</b>")
    $("img.slide").replaceWith("<img class='slide' src='static/images/welcome.jpg'>")
    $("span.classificationResult").replaceWith("<span style='color:#ff4000' class='classificationResult'>N/A</span>")
    $("span.accuracy").replaceWith("<span style='color:#ff4000' class='accuracy'>N/A</span>")
    $.ajax({
      url: '/trigger_detect',
      type: 'POST',
      contentType: 'application/json',
      dataType: 'text',
      data: JSON.stringify(myData),
      success: function(response) {
        // convert JSON object into javascript array
        var problem_list = $.parseJSON(response)
        console.log(problem_list[0])
        var arr_length = problem_list.length
        if(arr_length == 0) {
          alert("No Classification Result Returned\nPlease Check Your Image Format")
        }
        for(var i = 0; i < arr_length; ++i) {
          //console.log("iteration: " + i)
          var data = problem_list[i]
          var img_path = data[0]
          var labels = data[1]
          var accuracies = data[2]

          var labels_length = labels.length
          for(var j = 0; j < labels_length; ++j) {
            var temp = labels[j]
            labels[j] = temp.slice(2, -3)
          }

          img_path = img_path.slice(6, )

          /*console.log(img_path)
          console.log(labels[0])
          console.log(accuracies[0])*/

          var entry = {src: img_path, class: labels[0], accuracy: accuracies[0]}
          $("p.detectionLog").append("<div style='border-bottom:1px solid'>Detected <b style='color:#0055A2'>" + labels[0] + "</b> in image <a href='/static" + img_path + "'><img height='100' width='100' src='/static" + img_path + "'></a> with accuracy: <b style='color:#0055A2'>" + accuracies[0] + "</b></div>")
          $("b.oneTimeClassificationResult").replaceWith("<b class='oneTimeClassificationResult'>Detected <b style='color:#0055A2'>" + labels[0] + "</b> with accuracy: <b style='color:#0055A2'>" + accuracies[0] + "</b></b>")
          //$scope.photos.push(entry)
          if(accuracies[0] < threshold) {
            $("img.slide").replaceWith("<img class='slide' src='static" + img_path + "'>")
            $("span.classificationResult").replaceWith("<span style='color:#ff4000' class='classificationResult'>" + labels[0] + "</span>")
            $("span.accuracy").replaceWith("<span style='color:#ff4000' class='accuracy'>" + accuracies[0] + "</span>")
          }
        }
      },
      error: function(error) {
        console.log(error)
      }
    })
  }
  // functions handling object decisions
  $scope.findMattress = function() {
    var hasMattress = confirmationList[0];
    confirmationList[0] = !hasMattress;
  }
  $scope.findSofa = function() {
    var hasSofa = confirmationList[1];
    confirmationList[1] = !hasSofa;
  }
  $scope.findTvMonitor = function() {
    var hasTvMonitor = confirmationList[2];
    confirmationList[2] = !hasTvMonitor;
  }
  $scope.findFridge = function() {
    var hasFridge = confirmationList[3];
    confirmationList[3] = !hasFridge;
  }
  $scope.findChair = function() {
    var hasChair = confirmationList[4];
    confirmationList[4] = !hasChair;
  }
  $scope.findShoppingCart = function() {
    var hasShoppingCart = confirmationList[5];
    confirmationList[5] = !hasShoppingCart;
  }
  $scope.findCleanStreet = function() {
    var hasCleanStreet = confirmationList[6];
    confirmationList[6] = !hasCleanStreet;
  }
})

// Register the 'myCurrentTime' directive factory method.
app.directive('myCurrentTime', ['$interval', function($interval) {
// return the directive link function. (compile function not needed)
return function(scope, element) {
  var trainingTime = 0, // initial training time
  hours, mins, secs, millisecs,
  stopTime; // so that we can cancel the time updates

  // used to update the UI
  function updateTime() {
    trainingTime += 1000;
    //millisecs = parseInt(trainingTime % 1000);
    secs = trainingTime / 1000;
    mins = secs / 60;
    hours = parseInt(mins / 60);
    mins = parseInt(mins % 60);
    secs = parseInt(secs - hours * 3600 - mins * 60);
    element.text(hours + ":" + mins + ":" + secs);
  }

  stopTime = $interval(updateTime, 1000);

  // listen on DOM destroy (removal) event, and cancel the next UI update
  // to prevent updating time after the DOM element was removed.
  element.on('$destroy', function() {
    $interval.cancel(stopTime);
  });
}
}])

app.directive('myCurrentDataset', ['$interval', function($interval) {
// return the directive link function. (compile function not needed)
return function(scope, element) {
  var stopTime; // so that we can cancel the time updates

  // used to update the UI
  function updateSize() {
    $.ajax({
      url: '/getConfirmationStats',
      type: 'POST',
      success: function(response) {
        //console.log(response)
        // convert JSON object into javascript array
        var data = $.parseJSON(response);
        var datasetSize = "";
        for(var index = 0; index < data.length; ++index) {
          datasetSize = datasetSize + "<b style='color:#E5A823'>" + data[index][0] + "</b>" + " : " + data[index][1] + "<br>";
        }
        element.html(datasetSize);
      },
      error: function(error) {
        console.log(error)
      }
    })
  }

  // update per hour
  stopTime = $interval(updateSize, 1000);

  // listen on DOM destroy (removal) event, and cancel the next UI update
  // to prevent updating time after the DOM element was removed.
  element.on('$destroy', function() {
    $interval.cancel(stopTime);
  });
}
}])

app.directive()