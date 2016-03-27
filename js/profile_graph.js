function ProfileGraph(options) {
  this.ATTR_ID_MAP = {
    "Points": "points",
    "Goals": "goals",
    "Price": "price",
    "Assists": "assists",
    "Net transfers": "netTransfers",
    "Clean sheets": "cleanSheets",
    "Minutes played": "minutesPlayed",
    "Others": "others"
  };
  //Inverse map of the above
  this.ID_ATTR_MAP = (function(map) {
    var inverse_obj = {}
    for (let attr in map) { //attr is the key in ATTR_ID_MAP
      inverse_obj[map[attr]] = attr;
    }
    return inverse_obj
  })(this.ATTR_ID_MAP);

  for (let attr in this.ATTR_ID_MAP) {
    let MAP_REF = this.ATTR_ID_MAP;
    options.series.push({
      name: attr,
      id: MAP_REF[attr],
      type: "line",
      pointStart: 1
    });
  }
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
    minutesPlayed: new Array(38)
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

ProfileGraph.prototype.update = function(start, end) {
  var alertBox = $(".alert-danger");
  if (this.isValid()) {
    if (!alertBox.hasClass("hidden"))
      alertBox.toggleClass("hidden");
    // Clears the data in each series since events breakdown uses multiple series...
    this.graph.series.forEach(function(s) {
      s.setData([], false);
      s.show();
    });
    //Reference to the current graph's Highchart object for use inside the function call after this line
    var thisGraph = this;
    
    $("div.performance_metrics > .form-group:not(.hidden)").each(function() {
      thisGraph.graph.showLoading("Loading graph...");
      var attrMetricArray = $("select.form-control", this).val().split("-");
      var attr = attrMetricArray[0];
      var metric = attrMetricArray[1];
      if (metric === "over_time" || metric === "cum_total")
        thisGraph.drawLineGraph(attr, metric, start, end);
      else if (metric === "home_vs_away")
        thisGraph.drawPieChart(attr, metric, start, end);
      else if (metric === "consistency")
        thisGraph.drawBoxPlot(attr, metric, start, end);
      else if (metric === "events_breakdown")
        thisGraph.drawCompoundBarGraph(attr, metric, start, end);
      else if (metric === "changes")
        thisGraph.drawBarGraph(attr, metric, start, end);
      thisGraph.graph.hideLoading();
    });
  }
  else {
    if (alertBox.hasClass("hidden"))
      alertBox.toggleClass("hidden");
    else {
      alertBox.effect("highlight", {color: "#a94442"});
    }
  }
};

// Toggles the visibility of a serie. Returns true if the toggle shows the serie, otherwise false.
ProfileGraph.prototype.toggle = function(attr) {
  var serie = this.graph.get(attr);
  if (serie.visible)
    serie.hide();
  else
    serie.show();
};

//Trap: index starts from 0, so index (i-1) = week i (week 1 = index 0 etc)
ProfileGraph.prototype.drawLineGraph = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  this.graph.get(attr).update({
    data: requiredData,
    pointStart: 1,
    type: "line"
  }, false);
  this.graph.xAxis[0].update({
    categories: null,
    visible: true,
    title: {text: "Game weeks"}
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
};

ProfileGraph.prototype.drawPieChart = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  this.graph.get(attr).update({
    data: requiredData,
    type: "pie"
  }, false);
  this.graph.xAxis[0].update({
    visible: false
  }, false);
  this.graph.yAxis[0].update({
    visible: false
  }, false);
  this.graph.redraw();
};

ProfileGraph.prototype.drawBoxPlot = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  this.graph.get(attr).update({
    data: requiredData,
    type: "boxplot",
    pointStart: 1
  }, false);
  this.graph.xAxis[0].update({
    categories: [null, $("#player_name").text()],
    visible: false,
    title: {text: "Players"}
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
};

ProfileGraph.prototype.drawCompoundBarGraph = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  var thisGraph = this.graph; //The actual Highchart graph
  requiredData.forEach(function(dataObj) {
    var id = Object.getOwnPropertyNames(dataObj)[0];
    thisGraph.get(id).update({
      data: dataObj[id],
      type: "column",
      tooltip: {
        headerFormat: 'Event: <b>{series.name}</b><br>',
        pointFormat: '<b>Points:</b> {point.y}'
      },
      pointStart: 1
    }, false);
  });
  this.graph.xAxis[0].update({
    categories: null,
    visible: true,
    title: {text: "Game weeks"}
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
};

ProfileGraph.prototype.drawBarGraph = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  this.graph.get(attr).update({
    data: requiredData,
    type: "column",
    tooltip: {
      headerFormat: 'Week {point.key}<br>',
      pointFormat: '<b>Changes:</b> {point.y}'
    },
    pointStart: 1
  }, false);
  this.graph.xAxis[0].update({
    categories: null,
    visible: true,
    title: {text: "Game weeks"}
  }, false);
  this.graph.yAxis[0].update({
    visible: true
  }, false);
  this.graph.redraw();
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

// Checks whether the requested graoh to be drawn will be in a valid state
// An invalid state will be one where different, but incompatible graphs are being drawn
// on the same graph
// Examples: a pie chart together with a box plot since they both need the whole graph space, or
// a box plot together with line graphs since the box will cover up the lines/graph looks too clustered
ProfileGraph.prototype.isValid = function() {
  var valid = false;
  var dropdownsSelector = "div.performance_metrics > .form-group:not(.hidden) select.form-control";
  var selectedMetrics = [];
  $(dropdownsSelector).each(function() {
    var metric = $(this).val().split("-")[1];
    selectedMetrics.push(metric);
  });
  var metric_msg_map = {
    home_vs_away: "Home vs Away",
    consistency: "Consistency"
  };
  for (let metric of selectedMetrics) {
    if ((metric === "home_vs_away" || metric === "consistency") && selectedMetrics.length > 1) {
      var message = ('<b>'+metric_msg_map[metric]+'</b> cannot be selected when other drop down menus are visible. '+
        'Please hide the other drop down menu(s) before trying to select this option again.');
      $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+message);
      return valid;
    }
  }

  return !valid;
}
