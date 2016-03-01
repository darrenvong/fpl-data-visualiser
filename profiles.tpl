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

    <!-- Main part of the body to be filled -->
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
          <table class="table table-bordered">
            <thead>
              <tr class="thead-row-color">
                <th>Attribute</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Name</td>
                <td>Mahrez</td>
              </tr>
              <tr>
                <td>Points</td>
                <td>135</td>
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
            <div class="form-group">
              <label class="radio-inline">
                <input type="radio" name="performance_metric" id="consistency"> Consistency
              </label>
              <label class="radio-inline">
                <input type="radio" name="performance_metric" id="mean"> Mean
              </label>
              <label class="radio-inline">
                <input type="radio" name="performance_metric" id="accum_total"> Accumulative total
              </label>
              <!-- Do this feature if there's spare time... leaving it out for now -->
              <!-- <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span></button> -->
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
    <script>
      var playerNames = ["Mahrez", "Vardy", "Kane", "Sánchez"];
      var chart;

      function centerFormElement() {
        var inlineFormWidth = $('form.form-inline').width();
        $('.form-group').css("left", function(i, v) {
          return ( inlineFormWidth - $(this).width() )/2;
        });
      }
      centerFormElement();

      $("#player-names").autocomplete({
        source: playerNames,
        minLength: 0
      });
      $(document).ready(function() {
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
              }
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
              data: [[1, 15],[2, 10],[3, 10],[4, 1],[5, 11],[6, 11],[7, 2],[8, 0],[9, 4],[10, 6],[11, 15],[12, 2],[13, 9],[14, 2],[15, 21],[16, 13],[17, 15],[18, 2],[19, 3],[20, 1],[21, 3],[22, 1],[23, 6],[24, 6],[25, 14],[26, 1], [26.000001, 18]]
          }],
          credits: {
              enabled: false //Removes the highchart.com label at bottom right of graph
          }
        };
        chart = new Highcharts.Chart(graphOptions);

        $(window).resize(centerFormElement);
      });
    </script>
  </body>
</html>
