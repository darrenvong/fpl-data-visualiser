/** The top level function call (i.e. the main method) for the head to head comp page
 ** @author: Darren Vong
**/

$(document).ready(function() {
  centElement($('.form-group'),$('form.form-inline'));
  $(window).resize(function() {
      centElement($('.form-group'),$('form.form-inline'));
  });
  $("#more_options").click(function() {
    $(".attributes").toggleClass("hidden");
    centElement($('.form-group'),$('form.form-inline'));
    $("span:last-child", this).toggleClass("glyphicon-chevron-up glyphicon-chevron-down");
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
          pointFormat: ("<b>Min:</b> {point.low}<br/><b>Lower Quartile:</b> {point.q1}<br/>"+
            "<b>Median:</b> {point.median}<br/><b>Upper Quartile:</b> {point.q3}<br/><b>Max:</b> {point.high}<br/>")
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
  var graph = new HeadToHeadGraph(initOptions);

  $("#update_graph").click(function(e) {
    if ($("div.attributes").hasClass("hidden")) {
      return;
    }
    else if ($("input[type=checkbox]:checked").length === 0) { // Don't update graph if no "Active" checkboxes are ticked
      let message = 'Please tick one of the checkboxes above before clicking "Update graph" again.';
      inactiveError(e, message);
    }
    if (addUpdateGraphHandler())
      graph.update(gameWeekEndPoints[0], gameWeekEndPoints[1]);
  });

  $('[data-toggle="popover"]').popover();
});