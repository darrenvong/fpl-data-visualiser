function HeadToHeadGraph(options) {
  Highcharts.setOptions({
    lang: {loading: 'Click on <span class="glyphicon glyphicon-chevron-down"></span> to reveal the various plot options to begin!'}
  });

  this.initOptions = options;
  this.graph = new Highcharts.Chart(options);
  this.graph.showLoading();
  this.data = {
    points: new Array(38),
    price: new Array(38),
    goals: new Array(38),
    assists: new Array(38),
    cleanSheets: new Array(38)
  };

  var thisData = this.data;
  Object.keys(this.data).forEach(function(key) {
    var attrArray = thisData[key];
    for (var i=0; i < attrArray.length; i++) {
      attrArray[i] = new Array(38);
      for (var j=0; j < attrArray[i].length; j++) {
        attrArray[i][j] = {
          player1: null,
          player2: null
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
    $("input[type='radio']:checked", options).each(function() {
      var attr = $(this).attr("name");
      if ($(this).val() === "line")
        thisGraph.drawLineGraph(attr, start, end);
      else
        thisGraph.drawBarGraph(attr, start, end);
    });
  }
};

HeadToHeadGraph.prototype.toggle = function(start, end) {
  // body...
};

HeadToHeadGraph.prototype.get_data = function(attr, start, end) {
  var metric = "over_time";
};

HeadToHeadGraph.prototype.drawLineGraph = function(attr, start, end) {
  var metric = "over_time";
};

HeadToHeadGraph.prototype.drawBarGraph = function(attr, start, end) {
  var metric = "over_time";
};
