function HeadToHeadGraph(options) {
  Highcharts.setOptions({
    lang: {loading: 'Click on <span class="glyphicon glyphicon-chevron-down"></span> to reveal the various plot options to begin!'}
  });

  this.player1Name = $(".left figcaption").text();
  this.player2Name = $(".right figcaption").text();

  this.data = {
    points: new Array(38),
    price: new Array(38),
    goals: new Array(38),
    assists: new Array(38),
    cleanSheets: new Array(38)
  };

  var NAME_ATTR_MAP = {
    Points: "points",
    Price: "price",
    Goals: "goals",
    Assists: "assists",
    "Clean sheets": "cleanSheets"
  };
  var thisGraph = this;
  for (let attr in NAME_ATTR_MAP) {
    options.series.push({
      name: thisGraph.player1Name+"'s "+attr,
      id: "player1_"+NAME_ATTR_MAP[attr],
      pointStart: 1
    });
    options.series.push({
      name: thisGraph.player2Name+"'s "+attr,
      id: "player2_"+NAME_ATTR_MAP[attr],
      pointStart: 1
    });
  }
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
  var options = $("div.attributes");
  var metric = "over_time";
  var thisGraph = this;
  if (!options.hasClass("hidden")) {
    this.graph.showLoading("Loading graph...");
    var boxPlotSelected = false;
    $("input[type='radio']:checked", options).each(function() {
      //No other plots allowed when box plot selected since it doesn't work well on the same graph with other graph type
      if (boxPlotSelected)
        return;

      var thisRadio = $(this);
      var attr = thisRadio.attr("name");
      if (thisRadio.val() === "line") {
        thisGraph.drawLineGraph(attr, start, end);
      }
      else if (thisRadio.val() === "bar") {
        thisGraph.drawBarGraph(attr, start, end);
      }
      else { // Box plot selected for "Points"
        thisGraph.drawBoxPlot(attr, start, end);
        boxPlotSelected = true;
      }
    });
    this.graph.hideLoading();
  }
};

HeadToHeadGraph.prototype.toggle = function(start, end) {
  // body...
};

HeadToHeadGraph.prototype.getData = function(attr, start, end, metric) {
  if (metric === "consistency") {
    var player1Data = this.data[attr][start-1][end-1].player1.box;
    var player2Data = this.data[attr][start-1][end-1].player2.box;    
  }
  else {
    var player1Data = this.data[attr][start-1][end-1].player1.other;
    var player2Data = this.data[attr][start-1][end-1].player2.other;
  }

  if (player1Data && player2Data)
    return;
  else {
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
        var startEndMemBlock = thisGraph.data[attr][start-1][end-1].player1;
        if (metric === "consistency")
          startEndMemBlock.box = data[metric];
        else
          startEndMemBlock.other = data[metric];
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
        var startEndMemBlock = thisGraph.data[attr][start-1][end-1].player2;
        if (metric === "consistency")
          startEndMemBlock.box = data[metric];
        else
          startEndMemBlock.other = data[metric];
      }
    });
  }
};

HeadToHeadGraph.prototype.drawLineGraph = function(attr, start, end) {
  var metric = "over_time";
  this.getData(attr, start, end, metric);

  var instanceData = this.data;
  var player1Name = this.player1Name;
  var player2Name = this.player2Name;
  if (attr !== "price") {
    this.graph.get("player1_"+attr).update({
      data: instanceData[attr][start-1][end-1].player1.other,
      pointStart: 1,
      type: "line"
    }, false);
    this.graph.get("player2_"+attr).update({
      data: instanceData[attr][start-1][end-1].player2.other,
      pointStart: 1,
      type: "line"
    }, false);
  }
  else {
    this.graph.get("player1_"+attr).update({
      data: instanceData[attr][start-1][end-1].player1.other,
      pointStart: 1,
      type: "line",
      tooltip: {
        headerFormat: '',
        pointFormatter: function() {
          return ('Week '+Math.floor(this.x)+'<br><b>'+player1Name+
            '\'s Price:</b> £'+this.y+'M');
        }
      }
    }, false);
    this.graph.get("player2_"+attr).update({
      data: instanceData[attr][start-1][end-1].player2.other,
      pointStart: 1,
      type: "line",
      tooltip: {
        headerFormat: '',
        pointFormatter: function() {
          return 'Week '+Math.floor(this.x)+'<br><b>'+player2Name+
            '\'s Price:</b> £'+this.y+'M';
        }
      }
    }, false);
  }

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
};

HeadToHeadGraph.prototype.drawBoxPlot = function(attr, start, end) {
  var metric = "consistency";
};
