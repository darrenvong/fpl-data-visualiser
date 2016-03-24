/** The top level function call (i.e. the main method) for a player profiles' page
 ** @author: Darren Vong
**/

var initOptions = {
    chart: {
        renderTo: "graph_container",
        height: 500
    },
    title: {
        text: null
    },
    xAxis: {
        // title: {
        //     text: "Game weeks"
        // },
        minTickInterval: 1,
        allowDecimals: false
    },
    yAxis: {
        title: {
            text: null
        },
        allowDecimals: false
    },
    plotOptions: {
      line: {
        marker: {
          symbol: "circle"
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
        formatter: function() {
            return "Week "+Math.floor(this.x)+"<br><b>Points: </b>"+this.y;
        },
        followPointer: true
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

$(document).ready(function() {
  $("table.table-hover > tbody > tr:not(.no-extra-info)").each(function(){
    $(this).click(function() {
      // Switches the table rows between selected and unselected states
      $(this).toggleClass("info");
      var thisRowId = $(this).attr("id");
      var groupId = "#"+thisRowId+"_group";
      $(groupId).toggleClass("hidden");
      centElement($(groupId));
      if (thisRowId === "points" || thisRowId === "price") {
        var extrasId = "#"+thisRowId+"_extra";
        $(extrasId).toggleClass("hidden");
        $("span.glyphicon", this).toggleClass("glyphicon-chevron-right glyphicon-chevron-down");
      }
    });
  });
  centElement($('.form-group'));
  var searchBar = new PlayerSearchBar();

  $('button[type="submit"]').click(function(e) {
    searchBar.onSearch(e);
  });

  $('[data-toggle="popover"]').popover();
  
  $(window).resize(function() {
    centElement($('.form-group')); 
  });

  var graph = new ProfileGraph(initOptions);
});