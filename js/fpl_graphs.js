var chart;
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
        minTickInterval: 1
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

// For both draw and redraw, player names with space don't work and to be fixed...
// Also, correlate needs significant revamp for it to work.
// However as significant progress has been made on at least getting js to work
// with Python, Bottle and MongoDB, this buggy shall be pushed to a dev branch...
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
    chart.series[0].update({
        data: playersData[current],
        type: "line",
        pointStart: 1
    }, false);
    chart.setTitle({text: graphOptions.title.text});
    chart.xAxis[0].setTitle({text: graphOptions.xAxis.title.text});
    chart.yAxis[0].setTitle({text: graphOptions.yAxis.title.text});
    chart.redraw();
}

function drawBox() {
    var current = $('#players').val();
    var currentPlayerData = playersData[current];
    var median = math.median(currentPlayerData);
    var lq = math.quantileSeq(currentPlayerData, 0.25);
    var uq = math.quantileSeq(currentPlayerData, 0.75);
    var min = math.min(currentPlayerData);
    var max = math.max(currentPlayerData);
    // console.log("Median: "+median+"; LQ: "+lq+"; UQ: "+uq+"; min: "+min+"; max: "+max);
    chart.series[0].update({
        type: "boxplot",
        data: [[min, lq, median, uq, max]]
    }, false);
    chart.xAxis[0].setTitle({text: current});
    chart.yAxis[0].setTitle({text: graphOptions.yAxis.title.text});
    chart.redraw();
}

function drawCorr() {
    var current = $('#players').val();
    var current2 = $('#players2').val();
    var dataPair = playersData[current].map(function(e, i) {
        return [playersData[current][i], playersData[current2][i]];
    });
    chart.series[0].update({
        type: "scatter",
        data: dataPair
    }, false);
    chart.setTitle({text: "Relationship between "+current+" and "+current2});
    chart.xAxis[0].setTitle({text: current+"'s point"});
    chart.yAxis[0].setTitle({text: current2+"'s point"});
    chart.redraw();
}

$(document).ready(draw);
$(document).ready(function() {
    document.getElementById("drawline").addEventListener("click", myRedraw);
    document.getElementById("drawbox").addEventListener("click", drawBox);
    // document.getElementById("correlate").addEventListener("click", drawCorr);
});