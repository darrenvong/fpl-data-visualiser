function ProfileGraph(options) {
  var ATTR_ID_MAP = {
    "Points": "points",
    "Goals": "goals",
    "Price": "price",
    "Assists": "assists",
    "Net transfers": "netTransfers",
    "Clean sheets": "cleanSheets",
    "Minutes played": "minutesPlayed",
    "Others": "othersBreakdown",
    "Goals breakdown": "goalsBreakdown",
    "Assists breakdown": "assistsBreakdown",
    "Clean sheets breakdown": "cleanSheetsBreakdown"
  };
  //Inverse map of the above
  var ID_ATTR_MAP = (function(map) {
    var inverse_obj = {}
    for (let attr in map) { //attr is the key in ATTR_ID_MAP
      inverse_obj[map[attr]] = attr;
    }
    return inverse_obj
  })(ATTR_ID_MAP);

  for (let attr in ATTR_ID_MAP) {
    let MAP_REF = ATTR_ID_MAP;
    options.series.push({
      name: attr,
      id: MAP_REF[attr],
      type: "line",
      pointStart: 1,
      showInLegend: false
    });
  }
  this.initOptions = options;

  Highcharts.setOptions({
    lang: {loading: 'Click on <span class="glyphicon glyphicon-chevron-down"></span> to reveal the various plot options to begin!'}
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
  var graphValidity = this.isValid();
  toggleAlertBox(graphValidity);

  if (graphValidity) {
    // Clears the data in each series since events breakdown uses multiple series...
    this.graph.series.forEach(function(s) {
      s.setData([], false);
      s.update({showInLegend: false});
      s.show();
    });

    var options = $("div.performance_metrics");
    //Reference to the current graph instance for use inside the function call after this line
    var thisGraph = this;
    if (!options.hasClass("hidden")) {
      $("div.performance_metrics > .form-group").each(function() {
        var attrMetricArray = $("select.form-control", this).val().split("-");
        var attr = attrMetricArray[0];
        var metric = attrMetricArray[1];
        if ( $("input[type=checkbox]:checked", this).length === 0 ) {
          return;
        }
        else {
          thisGraph.graph.showLoading("Loading graph...");
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
        }
      });
    }
  }
};

// Toggles the visibility of a serie. Returns true if the toggle shows the serie, otherwise false.
ProfileGraph.prototype.toggle = function(attr, isBreakdown) {
  if (isBreakdown) { //Either defined or true
    var seriesToCheck = ["othersBreakdown","goalsBreakdown","assistsBreakdown","cleanSheetsBreakdown"];
    for (let i=0; i < seriesToCheck.length; i++) {
      var serie = this.graph.get(seriesToCheck[i]);
      if (serie.visible)
        serie.hide();
      else
        serie.show();
    }
  }
  else {
    var serie = this.graph.get(attr);
    if (serie.visible)
      serie.hide();
    else
      serie.show();    
  }
};

//Trap: index starts from 0, so index (i-1) = week i (week 1 = index 0 etc)
ProfileGraph.prototype.drawLineGraph = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  if (attr === "price") {
    this.graph.get(attr).update({
      data: requiredData,
      pointStart: 1,
      type: "line",
      tooltip: {
        headerFormat: '',
        // pointFormat: '<b>Price:</b> £{point.y}M'
        pointFormatter: function() {
          return 'Week '+Math.floor(this.x)+'<br><b>Price:</b> £'+this.y+'M';
        }
      },
      showInLegend: true
    }, false);
  }
  else {
    this.graph.get(attr).update({
      data: requiredData,
      pointStart: 1,
      type: "line",
      showInLegend: true
    }, false);
  }
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
    type: "pie",
    showInLegend: false
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
    pointStart: 1,
    showInLegend: false
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
    thisGraph.get(id+"Breakdown").update({
      data: dataObj[id],
      type: "column",
      tooltip: {
        headerFormat: '',
        // pointFormat: '<b>Points:</b> {point.y}'
        pointFormatter: function() {
          var seriesName = this.series.name.replace(" breakdown", "");
          return "Week "+Math.floor(this.x)+"<br>Event:<b> "+seriesName+"</b><br><b>Points:</b> "+this.y;
        }
      },
      pointStart: 1,
      showInLegend: true
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
      headerFormat: '',
      // pointFormat: '<b>Changes:</b> {point.y}M'
      pointFormatter: function() {
        return 'Week '+Math.floor(this.x)+'<br><b>Changes:</b> '+this.y+'M';
      }
    },
    pointStart: 1,
    showInLegend: true
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

ProfileGraph.prototype.getData = function(attr, metric, start, end, name) {
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
        player_name: name || $("img.img-responsive").attr("alt") //Added flexibility for inheritance
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

/** Checks whether the requested graoh to be drawn will be in a valid state
 ** An invalid state will be one where different, but incompatible graphs are being drawn
 ** on the same graph.
 ** Examples: a pie chart together with a box plot since they both need the whole graph space, or
 ** a box plot together with line graphs since the box will cover up the lines/graph looks too clustered
 **/
ProfileGraph.prototype.isValid = function() {
  var valid = true;
  var isBoxOrPieActive = false;
  var dropdownsSelector = "div.performance_metrics:not(.hidden) > .form-group select.form-control";
  var selectedMetrics = [];
  $(dropdownsSelector).each(function() {
    var metric = $(this).val().split("-")[1];
    selectedMetrics.push(metric);
  });
  var metric_msg_map = {
    home_vs_away: "Home vs Away",
    consistency: "Consistency"
  };

  if ((selectedMetrics.includes("home_vs_away") || selectedMetrics.includes("consistency")) && $(".points_switch:checked").length === 1)
    isBoxOrPieActive = true;

  if (isBoxOrPieActive && $("input[type=checkbox]:not(.points_switch):checked").length >= 1) {
      let metric = (selectedMetrics.includes("home_vs_away")) ? "home_vs_away" : "consistency";
      var message = ('<b>'+metric_msg_map[metric]+'</b> cannot be active at the same time with other options. '+
        'Please uncheck the "Active" box next to other drop down menu(s) or uncheck the "Active" box next to the dropdown with <b>'+metric_msg_map[metric]+
        '</b> selected before trying to select this option again.');
      $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+message);
      return !valid;
  }

  return valid;
}
