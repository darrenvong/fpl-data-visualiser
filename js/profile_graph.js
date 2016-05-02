/** A pseudoclass representing the graph object on the 'Player profiles' page.
 ** @author: Darren Vong
 **/

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

  this.ID_ATTR_MAP = (function(m) {
    var inverseMap = {}
    for (let attr in m) {
      inverseMap[m[attr]] = attr;
    }
    return inverseMap;
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
    lang: {loading: 'Tick one of the checkboxes next to "Active" in the options above then click "Update Graph" to begin!'}
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
    if (!options.hasClass("hidden") && $("input[type=checkbox]:checked").length !== 0) {
      $("div.performance_metrics > .form-group").each(function() {
        var attrMetricArray = $("select.form-control", this).val().split("-");
        var attr = attrMetricArray[0];
        var metric = attrMetricArray[1];
        if ( $("input[type=checkbox]:checked", this).length === 0 ) {
          return;
        }
        else {
          thisGraph.graph.showLoading("Loading graph...");
          thisGraph.graph.setTitle({text: null}, {text: "Click on any of the keys in the legend to toggle its corresponding graph line/bar's visibility"},false);
          if ((metric === "over_time" && attr === "cleanSheets") || metric === "changes")
            thisGraph.drawBarGraph(attr, metric, start, end);          
          else if (metric === "over_time" || metric === "cum_total")
            thisGraph.drawLineGraph(attr, metric, start, end);
          else if (metric === "home_vs_away")
            thisGraph.drawPieChart(attr, metric, start, end);
          else if (metric === "consistency")
            thisGraph.drawBoxPlot(attr, metric, start, end);
          else if (metric === "events_breakdown")
            thisGraph.drawCompoundBarGraph(attr, metric, start, end);
          thisGraph.graph.hideLoading();
        }
      });
    }
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
      tooltip: (attr === "points")? ({
        headerFormat: '{point.key}<br>',
        pointFormatter: function() {
          return 'Week '+Math.floor(this.x)+'<br><b>'+this.series.name+': </b>'+this.y;
        }
      }) : ({
        headerFormat: '',
        pointFormatter: function() {
          return 'Week '+Math.floor(this.x)+'<br><b>'+this.series.name+': </b>'+this.y;
        }
      }),
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
    tooltip: {
      headerFormat: '<b>{series.name}</b><br>',
      pointFormatter: function() {
        var data = this.series.data;
        if (data[0].percentage > data[1].percentage) { //"Home" portion of pie is greater than "Away"
          var largerPortion = {name: data[0].name, percentage: Math.round(data[0].percentage)};
        }
        else {
          var largerPortion = {name: data[1].name, percentage: Math.round(data[1].percentage)};
        }

        if (this.name === largerPortion.name)
          return '<span>'+largerPortion.percentage+'%</span>';
        else
          return '<span>'+(100-largerPortion.percentage)+'%</span>';
      }
    },
    showInLegend: false
  }, false);
  var attr_name_map = this.ID_ATTR_MAP;
  this.graph.xAxis[0].update({
    visible: false
  }, false);
  this.graph.yAxis[0].update({
    visible: false
  }, false);
  this.graph.setTitle({text: attr_name_map[attr]+" at Home vs Away"});
  this.graph.redraw();
};

ProfileGraph.prototype.drawBoxPlot = function(attr, metric, start, end) {
  var requiredData = this.getData(attr, metric, start, end);
  this.graph.get(attr).update({
    data: requiredData,
    type: "boxplot",
    pointStart: 1,
    tooltip: {
      headerFormat: "",
      pointFormatter: function() {
        return ("<b>Min:</b> "+this.low+"<br><b>Lower Quartile:</b> "+this.q1+"<br><b>Median:</b> "+
          this.median+"<br><b>Upper Quartile:</b> "+this.q3+"<br><b>Max:</b> "+this.high);
      }
    },
    showInLegend: false
  }, false);
  this.graph.xAxis[0].update({
    visible: false
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
    tooltip: (attr === "price")? ({
      headerFormat: '',
      // pointFormat: '<b>Changes:</b> {point.y}M'
      pointFormatter: function() {
        return 'Week '+Math.floor(this.x)+'<br><b>Changes:</b> '+this.y+'M';
      }      
    }) : ({
      headerFormat: '',
      pointFormatter: function() {
        return 'Week '+Math.floor(this.x)+'<br><b>'+this.series.name+': </b>'+this.y;
      }
    }),
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

ProfileGraph.prototype.getData = function(attr, metric, start, end) {
  var requiredData = this.data[attr][start-1][end-1];
  if (requiredData[metric]) {
    return requiredData[metric];
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
        requiredData[metric] = data[metric];
      },
      async: false
    });
    return requiredData[metric];
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
  var firstBoxOrPieSelected = null; //N.B. selected is not the same as having the "Active" box checked
  var dropdownsSelector = "div.performance_metrics:not(.hidden) > .form-group select.form-control";
  var selectedOptions = [];

  $(dropdownsSelector).each(function() {
    var selected = $(this).val().split("-");
    selectedOptions.push(selected);
  });

  var metric_msg_map = {
    home_vs_away: "Home vs Away",
    consistency: "Consistency"
  };

  for (let i = 0; i < selectedOptions.length; i++) {
    //selectedOptions[i][0] is the attribute, selectedOptions[i][1] is the metric
    let activeSelfCheck = "input."+selectedOptions[i][0]+"_switch[type=checkbox]:checked";
    //Attribute itself is active with box plot or pie chart selected and the total number of selected (active) checkboxes is not just itself
    if ($(activeSelfCheck).length === 1 && (selectedOptions[i][1] === "home_vs_away" || selectedOptions[i][1] === "consistency")
      && $("input[type=checkbox]:checked").length > 1) {
      let metric = (selectedOptions[i][1] === "home_vs_away") ? "home_vs_away" : "consistency";
      var message = ('<b>'+metric_msg_map[metric]+'</b> cannot be active at the same time with other options. '+
        'Please uncheck the "Active" box next to other drop down menu(s) or uncheck the "Active" box next to the dropdown with <b>'+metric_msg_map[metric]+
        '</b> selected before trying to update the graph.');
      $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+message);
      valid = false;
    }
  }

  return valid;
}
