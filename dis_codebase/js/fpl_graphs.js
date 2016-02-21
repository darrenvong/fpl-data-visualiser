var chart;
var playersData;
$.ajax({
      type: "POST",
      url: "/graphs",
      success: function(data) {
        playersData = data;
      },
      async: false
});
var graphOptions = {
    chart: {
        renderTo: "container",
        height: 500
    },
    title: {
        text: "FPL player's weekly score",
        x: -20 //center
    },
    xAxis: {
        title: {
            text: "Game weeks"
        },
        minTickInterval: 1,
        allowDecimals: false
    },
    yAxis: {
        title: {
            text: "Points"
        },
        allowDecimals: false
    },
    plotOptions: {
        line: {
            pointStart: 1
        }
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
            return "Week "+this.x+"<br><b>Points: </b>"+this.y;
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        borderWidth: 0,
        enabled: false
    },
    series: [],
    credits: {
        enabled: false //Removes the highchart.com label at bottom right of graph
    }
};

function draw() {
    var current = $('#players').val();
    graphOptions.series.push({
        data: playersData[current],
        name: current
    });
    chart = new Highcharts.Chart(graphOptions);
};

function myRedraw() {
    var current = $('#players').val();
    if (chart.series[0].type == "line") {
        chart.series[0].update({
            data: playersData[current],
            pointStart: 1
        }, false);
    }
    else {
        chart.series[0].update({
            data: playersData[current],
            type: "line",
            pointStart: 1
        }, false);
        chart.options.tooltip.formatter = graphOptions.tooltip.formatter;
    }
    chart.setTitle({text: graphOptions.title.text});
    chart.xAxis[0].setTitle({text: graphOptions.xAxis.title.text});
    chart.yAxis[0].setTitle({text: graphOptions.yAxis.title.text});
    chart.redraw();
}

function drawBox() {
    var current = $('#players').val();
    var currentPlayerData = playersData[current];
    currentPlayerData = currentPlayerData.map(function(e) {
        return e[1];
    });
    var median = math.median(currentPlayerData);
    var lq = math.quantileSeq(currentPlayerData, 0.25);
    var uq = math.quantileSeq(currentPlayerData, 0.75);
    var min = math.min(currentPlayerData);
    var max = math.max(currentPlayerData);
    // console.log("Median: "+median+"; LQ: "+lq+"; UQ: "+uq+"; min: "+min+"; max: "+max);
    chart.series[0].update({
        type: "boxplot",
        data: [[min, lq, median, uq, max]],
    }, false);
    chart.xAxis[0].setTitle({text: current.replace("_", " ")});
    chart.yAxis[0].setTitle({text: graphOptions.yAxis.title.text});
    chart.options.tooltip.formatter = function() {
        return "<b>LQ: </b>"+lq+"<br><b>Median: </b>"+median+"<br><b>UQ: </b>"+uq+
            "<br><b>Min: </b>"+min+"<br><b>Max: </b>"+max
    };
    chart.redraw();
}

function drawCorr() {
    var current1 = $('#players').val();
    var current2 = $('#players2').val();
    var current1Data = playersData[current1];
    var current2Data = playersData[current2];
    var dataPair = current1Data.map(function(e, i) {
            return [e[1], current2Data[i][1]];
        });
    chart.series[0].update({
        type: "scatter",
        data: dataPair
    }, false);
    chart.setTitle({text: "Relationship between "+current1+" and "+current2});
    chart.xAxis[0].setTitle({text: current1+"'s point"});
    chart.yAxis[0].setTitle({text: current2+"'s point"});
    chart.options.tooltip.formatter = function() {
        return current1+": "+this.x+"<br>"+current2+": "+this.y;
    }
    chart.redraw();
}

$(document).ready(draw);
$(document).ready(function() {
    document.getElementById("drawline").addEventListener("click", myRedraw);
    document.getElementById("drawbox").addEventListener("click", drawBox);
    document.getElementById("correlate").addEventListener("click", drawCorr);
});