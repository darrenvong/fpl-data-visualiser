function HeadToHeadGraph(options) {
  Highcharts.setOptions({
    lang: {loading: 'Click on <span class="glyphicon glyphicon-chevron-down"></span> to reveal the various plot options to begin!'}
  });

  this.player1Name = $(".left figcaption").text();
  this.player2Name = $(".right figcaption").text();

  this.data = {
    points: new Array(38),
    goals: new Array(38),
    assists: new Array(38),
    cleanSheets: new Array(38)
  };

  var NAME_ATTR_MAP = {
    Points: "points",
    Goals: "goals",
    Assists: "assists",
    "Clean sheets": "cleanSheets"
  };
  var thisGraph = this;
  for (let attr in NAME_ATTR_MAP) {
    options.series.push({
      name: thisGraph.player1Name+"'s "+attr,
      id: "player1_"+NAME_ATTR_MAP[attr],
      pointStart: 1,
      showInLegend: false
    });
    options.series.push({
      name: thisGraph.player2Name+"'s "+attr,
      id: "player2_"+NAME_ATTR_MAP[attr],
      pointStart: 1,
      showInLegend: false
    });
  }

  //An extra, one-off serie for box plot
  options.series.push({
    id: "box",
    showInLegend: false
  });

  this.initOptions = options;
  this.graph = new Highcharts.Chart(options);
  this.graph.showLoading();

  Object.keys(this.data).forEach(function(key) {
    var attrArray = thisGraph.data[key];
    for (var i=0; i < attrArray.length; i++) {
      attrArray[i] = new Array(38);
      for (var j=0; j < attrArray[i].length; j++) {
        attrArray[i][j] = {
          player1: {
            box: null,
            other: null
          },
          player2: {
            box: null,
            other: null
          }
        };
      }
    }
  });

}

HeadToHeadGraph.prototype.update = function(start, end) {
  var graphValidity = this.isValid();
  toggleAlertBox(graphValidity);

  if (graphValidity) {
    var options = $("div.attributes");
    var metric = "over_time";
    var thisGraph = this;
    if (!options.hasClass("hidden")) {
      this.graph.showLoading("Loading graph...");
      this.graph.series.forEach(function(s) {
        s.setData([], false);
        s.update({showInLegend: false});
        s.show();
      });
      $("input[type='radio']:checked", options).each(function() {
        var thisRadio = $(this);
        var attr = thisRadio.attr("name");
        if ($('.'+attr+'_switch:checked').length === 0) //Active checkbox not checked
          return;

        if (thisRadio.val() === "line") {
          thisGraph.drawLineGraph(attr, start, end);
        }
        else if (thisRadio.val() === "bar") {
          thisGraph.drawBarGraph(attr, start, end);
        }
        else { // Box plot selected for "Points"
          thisGraph.drawBoxPlot(attr, start, end);
        }
      });
      this.graph.hideLoading();
    }
    
  }
};

HeadToHeadGraph.prototype.toggle = function(start, end) {
  // body...
};

HeadToHeadGraph.prototype.updateData = function(attr, start, end, metric) {
  if (metric === "consistency") {
    var player1Data = this.data[attr][start-1][end-1].player1;
    var player2Data = this.data[attr][start-1][end-1].player2;
    if (player1Data.box && player2Data.box)
      return;
  }
  else {
    var player1Data = this.data[attr][start-1][end-1].player1;
    var player2Data = this.data[attr][start-1][end-1].player2;
    if (player1Data.other && player2Data.other)
      return;
  }

  var thisGraph = this;
  $.ajax("/graph_data", {
    method: "POST",
    data: {
      attr: attr,
      metric: metric,
      start: start,
      end: end,
      player_name: $(".left img").attr("alt")
    },
    async: false,
    success: function(data) {
      if (metric === "consistency")
        player1Data.box = data[metric][0];
      else
        player1Data.other = data[metric];
    }
  });
  $.ajax("/graph_data", {
    method: "POST",
    data: {
      attr: attr,
      metric: metric,
      start: start,
      end: end,
      player_name: $(".right img").attr("alt")
    },
    async: false,
    success: function(data) {
      if (metric === "consistency")
        //Since array of wanted data is wrapped in an array from API for single player graph
        player2Data.box = data[metric][0];
      else
        player2Data.other = data[metric];
    }
  });
};

HeadToHeadGraph.prototype.drawLineGraph = function(attr, start, end) {
  var metric = "over_time";
  this.updateData(attr, start, end, metric);

  var instanceData = this.data;
  var player1Name = this.player1Name;
  var player2Name = this.player2Name;

  this.graph.get("player1_"+attr).update({
    data: instanceData[attr][start-1][end-1].player1.other,
    pointStart: 1,
    type: "line",
    showInLegend: true
  }, false);
  this.graph.get("player2_"+attr).update({
    data: instanceData[attr][start-1][end-1].player2.other,
    pointStart: 1,
    type: "line",
    showInLegend: true
  }, false);
  this.graph.xAxis[0].update({
    categories: null,
    title: {text: "Game weeks"},
    visible: true
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
};

HeadToHeadGraph.prototype.drawBarGraph = function(attr, start, end) {
  var metric = "over_time";
  this.updateData(attr, start, end, metric);

  var instanceData = this.data;
  var player1Name = this.player1Name;
  var player2Name = this.player2Name;

  this.graph.get("player1_"+attr).update({
    data: instanceData[attr][start-1][end-1].player1.other,
    pointStart: 1,
    type: "column",
    showInLegend: true
  }, false);
  this.graph.get("player2_"+attr).update({
    data: instanceData[attr][start-1][end-1].player2.other,
    pointStart: 1,
    type: "column",
    showInLegend: true
  }, false);
  this.graph.xAxis[0].update({
    categories: null,
    title: {text: "Game weeks"},
    visible: true
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
};

HeadToHeadGraph.prototype.drawBoxPlot = function(attr, start, end) {
  var metric = "consistency";
  this.updateData(attr, start, end, metric);

  var instanceData = this.data;
  var player1Name = this.player1Name;
  var player2Name = this.player2Name;

  this.graph.get("box").update({
    data: [instanceData[attr][start-1][end-1].player1.box,
            instanceData[attr][start-1][end-1].player2.box],
    pointStart: 1,
    type: "boxplot",
    showInLegend: false
  }, false);
  this.graph.xAxis[0].update({
    categories: [null, player1Name, player2Name],
    title: {text: "Players"},
    visible: true
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
};

HeadToHeadGraph.prototype.isValid = function() {
  var boxSelected = false;
  var valid = true;
  $("input[type='radio']:checked").each(function() {
    var thisRadio = $(this);
    var attr = thisRadio.attr("name");
    var isActive = ($('.'+attr+'_switch:checked').length === 1)? true : false;
    if (!valid)
      return false; //Breaks the loop?

    //Box plot selected, active box checked. Second check is important since if active is not checked,
    //"technically" box is not selected
    if (thisRadio.val() === "box" && isActive) { //this will only be hit by "Points"
      boxSelected = true;
    }
    else if (isActive && boxSelected) { // Other attribute active whilst box plot selected
      valid = false;
    }
  });

  return valid;
};