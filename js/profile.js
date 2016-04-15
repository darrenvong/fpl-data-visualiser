/** The top level function call (i.e. the main method) for a player profiles' page
 ** @author: Darren Vong
**/

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
          pointFormatter: function() {
            return 'Week '+Math.floor(this.x)+'<br><b>'+this.series.name+': </b>'+this.y;
          }
        }
      },
      pie: {
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
        }
      },
      column: {
        stacking: "normal"
      },
      boxplot: {
        tooltip: {
          headerFormat: "",
          pointFormatter: function() {
            return ("<b>Min:</b> "+this.low+"<br><b>Lower Quartile:</b> "+this.q1+"<br><b>Median:</b> "+
              this.median+"<br><b>Upper Quartile:</b> "+this.q3+"<br><b>Max:</b> "+this.high);
          }
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

var graph;
$(document).ready(function() {
  $("table.table-hover > tbody > tr:not(.no-extra-info)").each(function(){
    $(this).click(function() {
      // Switches the table rows between selected and unselected states
      $(this).toggleClass("info");
      var thisRowId = $(this).attr("id");
      // var groupId = "#"+thisRowId+"_group";
      // $(groupId).toggleClass("hidden");
      // centElement($(groupId),$('form.form-inline'));
      if (thisRowId === "points" || thisRowId === "price") {
        var extrasId = "#"+thisRowId+"_extra";
        $(extrasId).toggleClass("hidden");
        $("span.glyphicon", this).toggleClass("glyphicon-chevron-right glyphicon-chevron-down");
      }
    });
  });

  $("#more_options").click(function() {
    $(".performance_metrics").toggleClass("hidden");
    centElement($('.form-group'),$('form.form-inline'));
    $("span:first-child","#more_options").toggleClass("glyphicon-chevron-down glyphicon-chevron-up");
  });

  centElement($('.form-group'),$('form.form-inline'));
  var searchBar = new PlayerSearchBar('#player-names');

  $('button[type="submit"]').click(function(e) {
    searchBar.onSearch(e, ['#player-names']);
  });

  hideErrorPrompts("#player-names");
  
  $(window).resize(function() {
    centElement($('.form-group'),$('form.form-inline')); 
  });

  graph = new ProfileGraph(initOptions);

  $("#update_graph").click(function() {
    var gameWeekEndPoints = addUpdateGraphHandler();
    if (gameWeekEndPoints)
      graph.update(gameWeekEndPoints[0], gameWeekEndPoints[1]);
  });
});
