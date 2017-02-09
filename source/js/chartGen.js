$(document).ready(function() {
// chart of system status
  var sysChart = c3.generate({
    bindto: '.sysChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['cpuUsage', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88]
      ],
      types: {
        cpuUsage: 'bar'   
      }
    },
    axis: {
      x: {
        type: 'timeseries',
        tick: {
            format: '%Y-%m-%d'
        }
      },
      y: {
        label: { // ADD
          text: 'CPU Usage',
          position: 'outer-middle'
        },
        tick: {
          format: d3.format(",%") // ADD
        }
      }
    }
  })

// chart of database status
  var dbChart = c3.generate({
    bindto: '.dbChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['matrix', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88],
        ['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]
      ]
    },
    axis: {
      x: {
        type: 'timeseries',
        tick: {
            format: '%Y-%m-%d'
        }
      },
      y: {
        label: { // ADD
          text: 'Image Storage',
          position: 'outer-middle'
        },
        tick: {
          format: d3.format(",%") // ADD
        }
      }
    }
  })

  // chart of neural network status
  var nnChart = c3.generate({
    bindto: '.nnChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['matrix', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88],
        ['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]
      ]
    },
    axis: {
      x: {
        type: 'timeseries',
        tick: {
            format: '%Y-%m-%d'
        }
      },
      y: {
        label: { // ADD
          text: 'Average Precisions',
          position: 'outer-middle'
        },
        tick: {
          format: d3.format(",%") // ADD
        }
      }
    }
  })

  // chart of client usage status
  var cuChart = c3.generate({
    bindto: '.cuChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['matrix', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88],
        ['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]
      ]
    },
    axis: {
      x: {
        type: 'timeseries',
        tick: {
            format: '%Y-%m-%d'
        }
      },
      y: {
        label: { // ADD
          text: 'Compelted Tasks',
          position: 'outer-middle'
        },
        tick: {
          format: d3.format(",%") // ADD
        }
      }
    }
  })

  // button clicks of System Status Chart
  $(".cpuUsage").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'CPU Usage'})
    sysChart.load({columns: [['cpuUsage', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88]]})
    sysChart.unload({ids: ['sofa']})
    document.getElementsByClassName('cpuUsage')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('memLoad')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('netTraff')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('cpuTemp')[0].style.backgroundColor = "#008CBA"
  })

  $(".memLoad").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'Memory Load'})
    sysChart.load({columns: [['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]]})
    sysChart.unload({ids: ['cpuUsage']})
    document.getElementsByClassName('cpuUsage')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('memLoad')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('netTraff')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('cpuTemp')[0].style.backgroundColor = "#008CBA"
  })

  $(".netTraff").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'Network Traffic'})
    sysChart.load({columns: [['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]]})
    sysChart.unload({ids: ['cpuUsage']})
    document.getElementsByClassName('cpuUsage')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('memLoad')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('netTraff')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('cpuTemp')[0].style.backgroundColor = "#008CBA"
  })

  $(".cpuTemp").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'CPU Temperature'})
    sysChart.load({columns: [['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]]})
    sysChart.unload({ids: ['cpuUsage']})
    document.getElementsByClassName('cpuUsage')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('memLoad')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('netTraff')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('cpuTemp')[0].style.backgroundColor = "#3ab795"
  })

  // button clicks of Database Status Chart
  $(".imgStorage").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    dbChart.axis.labels({y : 'Image Storage'})
    document.getElementsByClassName('imgStorage')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('dbIO')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('dbQuery')[0].style.backgroundColor = "#008CBA"
  })

  $(".dbIO").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    dbChart.axis.labels({y : 'I/O Traffic'})
    document.getElementsByClassName('imgStorage')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('dbIO')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('dbQuery')[0].style.backgroundColor = "#008CBA"
  })

  $(".dbQuery").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    dbChart.axis.labels({y : 'Database Queries'})
    document.getElementsByClassName('imgStorage')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('dbIO')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('dbQuery')[0].style.backgroundColor = "#3ab795"
  })

  // button clicks of Neural Network Status Chart
  $(".AP").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    nnChart.axis.labels({y : 'Average Precision'})
    document.getElementsByClassName('AP')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('datasetSize')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('detectedObjects')[0].style.backgroundColor = "#008CBA"
  })

  $(".datasetSize").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    nnChart.axis.labels({y : 'Dataset Size'})
    document.getElementsByClassName('AP')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('datasetSize')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('detectedObjects')[0].style.backgroundColor = "#008CBA"
  })

  $(".detectedObjects").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    nnChart.axis.labels({y : 'Detected Objects'})
    document.getElementsByClassName('AP')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('datasetSize')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('detectedObjects')[0].style.backgroundColor = "#3ab795"
  })

  // button clicks of Client Usage Status Chart
  $(".completedTasks").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    cuChart.axis.labels({y : 'Completed Tasks'})
    document.getElementsByClassName('completedTasks')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('supDec')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('upImg')[0].style.backgroundColor = "#008CBA"
  })

  $(".supDec").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    cuChart.axis.labels({y : 'Supervision Decisions'})
    document.getElementsByClassName('completedTasks')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('supDec')[0].style.backgroundColor = "#3ab795"
    document.getElementsByClassName('upImg')[0].style.backgroundColor = "#008CBA"
  })

  $(".upImg").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    cuChart.axis.labels({y : 'Upload Images'})
    document.getElementsByClassName('completedTasks')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('supDec')[0].style.backgroundColor = "#008CBA"
    document.getElementsByClassName('upImg')[0].style.backgroundColor = "#3ab795"
  })

  //set some initial styles of buttons
  document.getElementsByClassName("dataViews")[0].style.display = "none";
  document.getElementsByClassName("sysOpsButton")[0].style.backgroundColor = "#3ab795";
  document.getElementsByClassName("cpuUsage")[0].style.backgroundColor = "#3ab795";
  document.getElementsByClassName("imgStorage")[0].style.backgroundColor = "#3ab795";
  document.getElementsByClassName("AP")[0].style.backgroundColor = "#3ab795";
  document.getElementsByClassName("completedTasks")[0].style.backgroundColor = "#3ab795";
})