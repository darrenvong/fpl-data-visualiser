var graph;
$(document).ready(function() {
  centElement($('.form-group'),$('form.form-inline'));
  $(window).resize(function() {
      centElement($('.form-group'),$('form.form-inline'));
  });
  $("#more_options").click(function() {
    $(".attributes").toggleClass("hidden");
    centElement($('.form-group'),$('form.form-inline'));
  });

  var searchBars = new PlayerSearchBar("#player1, #player2");
  $("button[type='submit']").click(function(e) {
    searchBars.onSearch(e, ["#player1", "#player2"], true);
  });
  $("#player1_field, #player2_field").submit(function(e) {
    searchBars.onSearch(e, ["#player1", "#player2"], true);
  });
  hideErrorPrompts("#player1, #player2");

  var initOptions = {
    chart: {
        renderTo: "graph_container",
        height: 500
    },
    colors: ['#7cb5ec', '#90ed7d', '#f7a35c', '#8085e9',
              '#f15c80', '#2b908f', '#f45b5b', '#91e8e1'],
    title: {
        text: null
    },
    xAxis: {
        minTickInterval: 1,
        allowDecimals: false,
        visible: false
    },
    yAxis: {
        title: {
            text: null
        },
        allowDecimals: false,
        visible: false
    },
    plotOptions: {
      line: {
        marker: {
          symbol: "circle"
        },
        tooltip: {
          headerFormat: '{point.key}<br>',
          pointFormat: 'Week {point.x}<br><b>{series.name}: </b>{point.y}'
        }
      },
      column: {
        tooltip: {
          headerFormat: '{point.key}<br>',
          pointFormat: 'Week {point.x}<br><b>{series.name}: </b>{point.y}'
        }
      },
      boxplot: {
        tooltip: {
          headerFormat: "",
          pointFormat: ("<b>Min:</b> {point.low}<br/><b>LQ:</b> {point.q1}<br/>"+
            "<b>Median:</b> {point.median}<br/><b>UQ:</b> {point.q3}<br/><b>Max:</b> {point.high}<br/>")
        }
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
        followPointer: true,
    },
    legend: {
        align: 'right',
        verticalAlign: 'bottom',
        borderWidth: 0
    },
    series: [],
    credits: {
        enabled: false //Removes the highchart.com label at bottom right of graph
    }
  };
  graph = new HeadToHeadGraph(initOptions);

  $("#update_graph").click(addUpdateGraphHandler);

  $('[data-toggle="popover"]').popover();
});