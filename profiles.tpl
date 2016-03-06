<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="player profiles">
    <meta name="author" content="Darren Vong">
    <link rel="icon" href="img/favicon.ico">

    <title>Fantasy Premier League player Data Visualiser</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- jQuery UI CSS -->
    <link rel="stylesheet" href="css/jquery-ui.min.css">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/custom.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-default">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="index">Data Visualiser</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="index">Home</a></li>
            <li><a href="#">About</a></li>
            <li class="dropdown">
              <a href="#" id="tools-dd" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                Tools
                <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="#">Player profiles</a></li>
                <li><a href="#">Head-to-head comparator</a></li>
                <li><a href="#">Multi-player comparator</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main "body" of the page -->
    <div class="container profile-body">
      <div class="row">
        <div class="col-md-5">
          <label for="player-names">Player's name: </label>
          <input id="player-names" type="text" size="20">
          <button type="button" class="btn btn-default">
            <span class="sr-only">Search</span>
            <span class="glyphicon glyphicon-search"></span>
          </button>
          <figure>
            <img src="faces/Mahrez.jpg" class="img-responsive center-block" alt="Mahrez">
          </figure>
          <p class="text-center"><b>Mahrez</b></p>
          <caption>Click on a row to project more details to the graph.</caption>
          <table class="table table-bordered table-hover">
            <thead>
              <tr class="thead-row-color">
                <th>Attribute</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr id="points">
                <td>Points</td>
                <td>135</td>
              </tr>
              <tr id="goals">
                <td>Goals</td>
                <td>14</td>
              </tr>
              <tr id="assists">
                <td>Assists</td>
                <td>18</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="col-md-7">
          <form class="form-inline">
            <div class="form-group" id="gameweek">
              <label for="time-frame">From Game Week: </label>
              <select id="startTime" class="form-control sm-screen">
                % for wk in xrange(1,28):
                <option value={{wk}}>{{wk}}</option>
                % end
              </select>&nbsp;&nbsp;TO&nbsp;&nbsp;
              <select id="endTime" class="form-control sm-screen">
                % for wk in xrange(1,28):
                <option value={{wk}}>{{wk}}</option>
                % end
              </select>
              <button type="button" class="btn btn-default" id="update_graph"><span class="glyphicon glyphicon-refresh"></span> Update graph</button>
            </div>
            <div class="form-group" id="points_group">
              <label class="labels">Points:</label>
              <select class="form-control">
                <option value="points-over_time">Over selected game weeks</option>
                <option value="points-consistency">Consistency</option>
                <option value="points-mean">Mean</option>
                <option value="points-accum_total">Cumulative total</option>
              </select>
              <button type="button" class="btn btn-danger btn-sm" aria-label="Remove attribute from graph"><span class="glyphicon glyphicon-remove"></span></button>
              <a role="button" class="btn" data-toggle="popover" title="Points" data-content="Lorem ipsum..." data-trigger="hover" data-placement="right"><span class="glyphicon glyphicon-info-sign"></span></a>
              <!-- Do this feature if there's spare time... leaving it out for now -->
              <!-- <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span></button> -->
            </div><br>
            <div class="form-group hidden" id="goals_group">
              <label class="labels">Goals:</label>
              <select class="form-control">
                  <option value="goals-over_time"> Over selected game weeks</option>
                  <option value="goals-home_vs_away"> Home vs Away</option>
                  <option value="goals-accum_total"> Cumulative total</option>
                  <option value="goals-running_mean"> Running mean</option>
              </select>
              <button type="button" class="btn btn-danger btn-sm" aria-label="Remove attribute from graph"><span class="glyphicon glyphicon-remove"></span></button>
              <a role="button" class="btn" data-toggle="popover" title="Goals" data-content="Lorem ipsum..." data-trigger="hover" data-placement="right"><span class="glyphicon glyphicon-info-sign"></span></a>
            </div>
          </form>
            <div id="graph_container"></div>
        </div> <!-- end of col-md-7 (aka the right column) -->
      </div>

      <footer class="footer">
        <p>&copy; Darren Vong 2016</p>
      </footer>
    </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="js/jquery-2.1.4.min.js"><\/script>')</script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/jquery-ui.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
    <script src="js/highcharts.js"></script>
    <script src="js/highcharts-more.js"></script>
    <script src="js/modules/no-data-to-display.js"></script>
    <script src="js/math.min.js"></script>
    <script>
      var playerNames = ["Mahrez", "Vardy", "Kane", "Sánchez"];
      var chart;
      var playersData = [[1, 15],[2, 10],[3, 10],[4, 1],[5, 11],[6, 11],[7, 2],[8, 0],[9, 4],[10, 6],[11, 15],[12, 2],[13, 9],[14, 2],[15, 21],[16, 13],[17, 15],[18, 2],[19, 3],[20, 1],[21, 3],[22, 1],[23, 6],[24, 6],[25, 14],[26, 1], [28, 18]];
      var graphOptions = {
          chart: {
              renderTo: "graph_container",
              height: 500
          },
          title: {
              text: "FPL player's weekly score"
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
          series: [{
              // data: [15,10,10,1,11,11,2,15,10,10,1,11,11,2,15,10,10,1,11,11,2,21,15,8,3,2]
              data: playersData,
              name: "Points"
          }],
          credits: {
              enabled: false //Removes the highchart.com label at bottom right of graph
          }
        };
      
      function centElement(elements) {
        var inlineFormWidth = $('form.form-inline').width();
        elements.css("left", function(i,v) {
          return ( inlineFormWidth - $(this).width() ) / 2;
        });
      }

      /* Start/end time here is optional, as with all js functions */
      function drawConsBox(start, end) {
        if (start > end) {
          alert("Can't have start time later than end time!");
          return;
        }
        var data = playersData.filter(function(e) {
          return e[0] >= start && e[0] <= end;
        }).map(function(e) {
          return e[1];
        });
        var median = math.median(data);
        var lq = math.quantileSeq(data, 0.25);
        var uq = math.quantileSeq(data, 0.75);
        var min = math.min(data);
        var max = math.max(data);

        if (chart.series.length === 0) {
          chart.addSeries({
            type: "boxplot",
            data: [[min, lq, median, uq, max]],
            name: "Points",
            color: chart.options.colors[0]
          }, false);
        }
        else {
          chart.series[0].update({
            type: "boxplot",
            data: [[min, lq, median, uq, max]]
          }, false);
        }

        chart.xAxis[0].update({
          categories: [null, "Mahrez"], // Since category values are taken from index 0
          title: {text: "Player's name"},
        }, false);
        chart.options.tooltip.formatter = function() {
        return "<b>LQ: </b>"+lq+"<br><b>Median: </b>"+median+"<br><b>UQ: </b>"+uq+
            "<br><b>Min: </b>"+min+"<br><b>Max: </b>"+max
        };
        chart.redraw();
      }

      function clearGraph() {
        if (chart.series[0].name === "Points")
          chart.series[0].remove();
      }

      centElement($('.form-group'));

      $("#player-names").autocomplete({
        source: playerNames,
        minLength: 0
      });
      $(document).ready(function() {
        chart = new Highcharts.Chart(graphOptions);

        $(window).resize(function() {
          centElement($('.form-group')); 
        });
        $("table.table-hover > tbody > tr").click(function() {
          $(this).toggleClass("info");
        });
        $("#goals").click(function() {
          $("#goals_group").toggleClass("hidden");
          centElement($('.form-group'));
        });
        $("#points_group > button").click(clearGraph);
        $("#update_graph").click(function() {
          if ( $("#points_group > select.form-control").val() === "points-consistency") {
            var start = parseInt($("#startTime").val());
            var end = parseInt($("#endTime").val());
            drawConsBox(start, end);            
          }
        });
        $('[data-toggle="popover"]').popover();
      });
    </script>
  </body>
</html>
