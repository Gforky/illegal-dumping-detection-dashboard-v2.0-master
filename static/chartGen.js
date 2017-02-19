$(document).ready(function() {
  var blue = "#0055A2", gold = "#E5A823", white = "#ffffff";
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
  })

  $(".memLoad").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'Memory Load'})
    sysChart.load({columns: [['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]]})
    sysChart.unload({ids: ['cpuUsage']})
  })

  $(".netTraff").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'Network Traffic'})
    sysChart.load({columns: [['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]]})
    sysChart.unload({ids: ['cpuUsage']})
  })

  $(".cpuTemp").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    sysChart.axis.labels({y : 'CPU Temperature'})
    sysChart.load({columns: [['sofa', 0.76, 0.85, 0.96, 0.97, 0.86, 0.78]]})
    sysChart.unload({ids: ['cpuUsage']})
  })

  // button clicks of Database Status Chart
  $(".imgStorage").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    dbChart.axis.labels({y : 'Image Storage'})
  })

  $(".dbIO").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    dbChart.axis.labels({y : 'I/O Traffic'})
  })

  $(".dbQuery").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    dbChart.axis.labels({y : 'Database Queries'})
  })

  // button clicks of Neural Network Status Chart
  $(".AP").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    nnChart.axis.labels({y : 'Average Precision'})
  })

  $(".datasetSize").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    nnChart.axis.labels({y : 'Dataset Size'})
  })

  $(".detectedObjects").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    nnChart.axis.labels({y : 'Detected Objects'})
  })

  // button clicks of Client Usage Status Chart
  $(".completedTasks").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    cuChart.axis.labels({y : 'Completed Tasks'})
  })

  $(".supDec").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    cuChart.axis.labels({y : 'Supervision Decisions'})
  })

  $(".upImg").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    cuChart.axis.labels({y : 'Upload Images'})
  })
})