var playerNames = ["Mahrez", "Vardy", "Kane", "Sánchez"];
var chart;
var playersData = [[1, 15],[2, 10],[3, 10],[4, 1],[5, 11],[6, 11],[7, 2],[8, 0],[9, 4],[10, 6],[11, 15],[12, 2],[13, 9],[14, 2],[15, 21],[16, 13],[17, 15],[18, 2],[19, 3],[20, 1],[21, 3],[22, 1],[23, 6],[24, 6],[25, 14],[26, 1], [28, 18]];
var initOptions = {
    chart: {
        renderTo: "graph_container",
        height: 500
    },
    title: {
        text: null
    },
    xAxis: {
        // title: {
        //     text: "Game weeks"
        // },
        minTickInterval: 1,
        allowDecimals: false
    },
    yAxis: {
        title: {
            text: null
        },
        allowDecimals: false
    },
    exporting: {
        buttons: {
            contextButton: {
                enabled: false
            }
        }
    },
    tooltip: {
        formatter: function() {
            return "Week "+Math.floor(this.x)+"<br><b>Points: </b>"+this.y;
        },
        followPointer: true
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        borderWidth: 0,
        enabled: false
    },
    series: [{
        name: "Points"
    }],
    credits: {
        enabled: false //Removes the highchart.com label at bottom right of graph
    }
  };


function centElement(elements) {
  var inlineFormWidth = $('form.form-inline').width();
  elements.css("left", function(i,v) {
    return ( inlineFormWidth - $(this).width() ) / 2;
  });
}

function drawConsBox(start, end) {
  var data = playersData.filter(function(e) {
    return e[0] >= start && e[0] <= end;
  }).map(function(e) {
    return e[1];
  });
  var median = math.median(data);
  var lq = math.quantileSeq(data, 0.25);
  var uq = math.quantileSeq(data, 0.75);
  var min = math.min(data);
  var max = math.max(data);

  if (chart.series.length === 0) {
    chart.addSeries({
      type: "boxplot",
      data: [[min, lq, median, uq, max]],
      name: "Points",
      color: chart.options.colors[0]
    }, false);
  }
  else {
    chart.series[0].update({
      type: "boxplot",
      data: [[min, lq, median, uq, max]]
    }, false);
  }

  chart.xAxis[0].update({
    categories: [null, "Mahrez"], // Since category values are taken from index 0
    title: {text: "Player's name"},
  }, false);
  chart.options.tooltip.formatter = function() {
  return "<b>LQ: </b>"+lq+"<br><b>Median: </b>"+median+"<br><b>UQ: </b>"+uq+
      "<br><b>Min: </b>"+min+"<br><b>Max: </b>"+max
  };
  chart.redraw();
}

function drawLineGraph(start, end) {
  var reformedData = playersData.filter(function(e) {
    return e[0] >= start && e[0] <= end;
  }).map(function(e) {
    return e[1];
  });

  if (chart.series.length === 0) {
    chart.addSeries({
      data: reformedData,
      name: "Points",
      color: chart.options.colors[0],
      pointStart: 1,
      type: "line"
    }, false);
    chart.xAxis[0].update({
      title: {text: "Game weeks"},
      categories: null
    }, false);
    chart.yAxis[0].update({
      title: {text: "Points"}
    }, false);
    chart.options.tooltip.formatter = initOptions.tooltip.formatter;
    chart.redraw();
  }
  else {
    chart.series[0].update({
      data: reformedData,
      pointStart: 1,
      type: "line"
    }, false);
    chart.xAxis[0].update({
      title: {text: "Game weeks"},
      categories: null
    }, false);
    chart.yAxis[0].update({
      title: {text: "Points"}
    }, false);
    chart.options.tooltip.formatter = initOptions.tooltip.formatter;
    chart.redraw();
  }
}

function clearGraph() {
  if (chart.series[0].name === "Points")
    chart.series[0].remove();
}

centElement($('.form-group'));

$("#player-names").autocomplete({
  source: playerNames,
  minLength: 0
});

function masterDraw(metric, start, end) {
  if (metric === "points-consistency")
    drawConsBox(start, end);
  else if (metric === "points-over_time")
    drawLineGraph(start, end);
}

$(document).ready(function() {
  Highcharts.setOptions({
    lang: {noData: "Select a row on the table to begin!"}
  });
  chart = new Highcharts.Chart(initOptions);

  $(window).resize(function() {
    centElement($('.form-group')); 
  });
  // Switches the table rows between selected and unselected states
  $("table.table-hover > tbody > tr").click(function() {
    $(this).toggleClass("info");
  });
  $("table.table-bordered > tbody > tr").each(function(){
    $(this).click(function() {
      var group_id = "#"+$(this).attr("id")+"_group";
      $(group_id).toggleClass("hidden");
      centElement($(group_id));           
    });
  });
  // An example of clicking a specific row which updates the metric options
  // $("#goals").click(function() {
  //   $("#goals_group").toggleClass("hidden");
  //   centElement($('.form-group'));
  // });

  // Example of clicking a specific attribute (i.e. goals, assists etc)
  $("#points_group > button").click(clearGraph);
  // Example of updating the graph to a different type when different metric selected AND "update graph" button clicked
  $("#update_graph").click(function() {
    var start = parseInt($("#startTime").val());
    var end = parseInt($("#endTime").val());
    if (start > end) {
      alert("Can't have start time later than end time!");
      return;
    }
    
    var optionsSuffix = ["-over_time", "-consistency"];
    $("div.performance_metrics > .form-group:not(.hidden)").each(function() {
      var valsToCheck = [];
      // Foreach loop is 'for.. of' in js because it is weird... 
      for (suffix of optionsSuffix) {
        valsToCheck.push($(this).attr("id").split("_")[0]+suffix);
      }
      for (v of valsToCheck) {
        var selectedValue = $("select.form-control", this).val();
        if ( selectedValue === v ) {
          masterDraw(v, start, end);
          return; //can only have one val, so quit loop when val found
        }
      }
    });

    // This is a specific example
    // if ( $("#points_group > select.form-control").val() === "points-consistency" )
    //   drawConsBox(start, end);
  });
  $('[data-toggle="popover"]').popover();
});