$(document).ready(function() {
  var blue = "#0055A2", gold = "#E5A823", white = "#ffffff";
// chart of system status
  var sysChartConfig = {
    bindto: '.sysChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['CPU Usage', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88]
      ],
      type: 'bar'
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
  }

  var sysChart = c3.generate(sysChartConfig)

// chart of database status
  var dbChartConfig = {
    bindto: '.dbChart',
    data: {
      x : 'x',
      columns: [['x', 0], ['mattress', 298], ['sofa', 276], ['tv-monitor', 198]],
      type : 'pie'
    },
    pie: {
      label: {
        format: function (value, ratio, id) {
          return d3.format('')(value);
        }
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
          text: 'Compelted Tasks',
          position: 'outer-middle'
        },
        tick: {
          format: function (d) { return d + "queries/second"; } // ADD
        }
      }
    }
  }

  var dbChart = c3.generate(dbChartConfig)

  // chart of neural network status
  var nnChartConfig = {
    bindto: '.nnChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['mattress', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88],
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

  var nnChart = c3.generate(nnChartConfig)

  // chart of client usage status
  var cuChartConfig = {
    bindto: '.cuChart',
    data: {
      x : 'x',
      columns: [
        ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        ['mattress', 0.55, 0.80, 0.70, 0.68, 0.98, 0.88],
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
  }

  var cuChart = c3.generate(cuChartConfig)
  
  // button clicks of System Status Chart
  $(".cpuUsage").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    $.ajax({
      url: '/getCpuUsage',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        sysChart.axis.labels({y : 'CPU Usage'})
        //sysChart.transform('bar');
        sysChart.load({
          columns: $.parseJSON(response), 
          type: 'bar'})
        sysChart.unload({ids: ['Memory Load', 'Network Traffic', 'CPU Temperature']})
      },
      error: function(error) {
        console.log(error)
      }
    })
  })

  $(".memLoad").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    $.ajax({
      url: '/getMemLoad',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        sysChart.axis.labels({y : 'Memory Load'})
        //sysChart.transform('bar');
        sysChart.load({
          columns: $.parseJSON(response), 
          type: 'line'})
        sysChart.unload({ids: ['CPU Usage', 'Network Traffic', 'CPU Temperature']})
      },
      error: function(error) {
        console.log(error)
      }
    })
  })

  $(".netTraff").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    $.ajax({
      url: '/getNetTraff',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        sysChart.axis.labels({y : 'Network Traffic'})
        //sysChart.transform('bar');
        sysChart.load({
          columns: $.parseJSON(response), 
          type: 'line'})
        sysChart.unload({ids: ['CPU Usage', 'Memory Load', 'CPU Temperature']})
      },
      error: function(error) {
        console.log(error)
      }
    })
  })

  $(".cpuTemp").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    $.ajax({
      url: '/getCpuTemp',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        sysChart.axis.labels({y : 'CPU Temperature'})
        //sysChart.transform('bar');
        sysChart.load({
          columns: $.parseJSON(response), 
          type: 'line'})
        sysChart.unload({ids: ['CPU Usage', 'Memory Load', 'Network Traffic']})
      },
      error: function(error) {
        console.log(error)
      }
    })
  })

  // button clicks of Database Status Chart
  $(".imgStorage").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    //dbChart.axis.labels({y : 'Image Storage'})
    $.ajax({
      url: '/getImgStorage',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        //sysChart.transform('bar');
        dbChart.transform('pie')
        dbChart.load({
          columns: $.parseJSON(response), 
          type: 'pie'})
        dbChart.unload({ids: ['Database I/O Traffic', 'Database Queries']})
      },
      error: function(error) {
        console.log(error)
      }
    })
  })

  $(".dbIO").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    //dbChart.axis.labels({y : 'I/O Traffic'})
    $.ajax({
      url: '/getDBIO',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        //sysChart.transform('bar');
        dbChartConfig.axis.y.tick = { format : function (d) { return d + "queries/second"; } }
        dbChart.transform('line')
        dbChart.load({
          columns: $.parseJSON(response), 
          type: 'line'})
        dbChart.axis.labels({ y : 'Database I/O Traffic'})
        dbChart.unload({ids: ['mattress', 'sofa', 'tv-monitor', 'Database Queries']})
      },
      error: function(error) {
        console.log(error)
      }
    })
  })

  $(".dbQuery").click(function() {
    //chart.axis.ticks{x : {format: '%Y-%m-%d'}, y : {format: d3.format(",%")}}
    //dbChart.axis.labels({y : 'Database Queries'})
    $.ajax({
      url: '/getDBQuery',
      type: 'POST',
      success: function(response) {
        console.log(response)
        // convert JSON object into javascript array
        //sysChart.transform('bar');
        dbChartConfig.axis.y.tick = { format : function (d) { return d + "queries"; } }
        dbChart = c3.generate(dbChartConfig)
        dbChart.transform('line')
        dbChart.load({
          columns: $.parseJSON(response),
          type: 'line'})
        dbChart.axis.labels({ y : 'Database Queries'})
        dbChart.unload({ids: ['mattress', 'sofa', 'tv-monitor', 'Database I/O Traffic']})
      },
      error: function(error) {
        console.log(error)
      }
    })
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