function ProfileGraph(options) {
  this.initOptions = options;

  Highcharts.setOptions({
    lang: {loading: "Select a row on the table to begin!"}
  });

  this.graph = new Highcharts.Chart(options);
  this.graph.showLoading();
  this.data = {
    points: new Array(38),
    price: new Array(38),
    goals: new Array(38),
    assists: new Array(38),
    netTransfers: new Array(38),
    minsPlayed: new Array(38)
  };
  if ($('#cleanSheets').length !== 0)
    this.data.cleanSheets = new Array(38);
  
  var thisData = this.data;
  Object.keys(this.data).forEach(function(key) {
    var attrArray = thisData[key];
    for (var i=0; i < attrArray.length; i++) {
      attrArray[i] = new Array(38);
      for (var j=0; j < attrArray[i].length; j++) {
        attrArray[i][j] = {
          over_time: undefined,
          home_vs_away: undefined,
          consistency: undefined,
          cum_total: undefined,
          events_breakdown: undefined,
          changes: undefined
        };
      }
    }
  });
}

ProfileGraph.prototype.clear = function() {
  // body...
};

//Trap: index starts from 0, so index (i-1) = week i (week 1 = index 0 etc)
ProfileGraph.prototype.drawLineGraph = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  if (this.graph.series.length === 0) {
    this.graph.addSeries({
      data: requiredData,
      name: "Points",
      id: "points",
      color: this.graph.options.colors[0],
      pointStart: 1,
      type: "line"
    }, false);
    this.graph.xAxis[0].update({
      title: {text: "Game weeks"},
      categories: null
    }, false);
    this.graph.yAxis[0].update({
      title: {text: "Points"}
    }, false);
    this.graph.redraw();
  }
  else {
    this.graph.series[0].update({
      data: requiredData,
      pointStart: 1,
      type: "line"
    }, false);
    this.graph.xAxis[0].update({
      title: {text: "Game weeks"},
      categories: null
    }, false);
    this.graph.yAxis[0].update({
      title: {text: "Points"}
    }, false);
    this.graph.options.tooltip.formatter = initOptions.tooltip.formatter;
    this.graph.redraw();
  }
};

ProfileGraph.prototype.drawPieChart = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
};

ProfileGraph.prototype.getData = function(attr, metric, start, end) {
  var myData = this.data[attr][start-1][end-1][metric];
  if (myData) {
    return myData;
  }
  else {
    var thisData = this.data;
    $.ajax("/graph_data", {
      method: "POST",
      data: {
        attr: attr,
        metric: metric,
        start: start,
        end: end,
        player_name: $("img.img-responsive").attr("alt")
      },
      success: function(data) {
        var startEndMemBlock = thisData[attr][start-1][end-1];
        startEndMemBlock[metric] = data[metric];
        myData = data[metric];
      },
      async: false
    });
    return myData;
  }
};

ProfileGraph.prototype.update = function(start, end) {
  this.graph.showLoading("Loading graph...");
  //Perform the updates...
  var thisGraph = this;
  $("div.performance_metrics > .form-group:not(.hidden)").each(function() {
    var attrMetricArray = $("select.form-control", this).val().split("-");
    var attr = attrMetricArray[0];
    var metric = attrMetricArray[1];
    if (metric === "over_time" || metric === "cum_total")
      thisGraph.drawLineGraph(attr, metric, start, end);
    else if (metric === "home_vs_away")
      thisGraph.drawPieChart(attr, metric, start, end);
  });
  this.graph.hideLoading();
};

// --------------------------- Codes below here to be rewritten to fit into ProfileGraph --------------------------- //
var playersData = [[1, 15],[2, 10],[3, 10],[4, 1],[5, 11],[6, 11],[7, 2],[8, 0],[9, 4],[10, 6],
                    [11, 15],[12, 2],[13, 9],[14, 2],[15, 21],[16, 13],[17, 15],[18, 2],[19, 3],
                    [20, 1],[21, 3],[22, 1],[23, 6],[24, 6],[25, 14],[26, 1], [27, 18]];

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

function clearGraph() {
  if (chart.series[0].name === "Points")
    chart.series[0].remove();
}

function masterDraw(metric, start, end) {
  if (metric === "points-consistency")
    drawConsBox(start, end);
  else if (metric === "points-over_time")
    drawLineGraph(start, end);
}
