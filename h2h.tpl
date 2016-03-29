<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="Head to head player comparator">
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
    <link href="css/general.css" rel="stylesheet">
    <link href="css/head_to_head.css" rel="stylesheet">

    <!-- Polyfill fixes by Mozilla Developer Network (2016), https://developer.mozilla.org/ -->
    <script src="js/polyfills.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar">
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
                <li><a href="profile">Player profiles</a></li>
                <li><a href="head_to_head">Head-to-head comparator</a></li>
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
        <div class="col-md-3 left">
          <div class="input-group">
            <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
            <input id="player1" class="form-control" name="player1" type="search">
          </div>
          <figure>
            <img src="faces/78830.jpg" class="img-responsive center-block" alt='Harry Kane'>
          </figure>
          <figcaption class="text-center"><b>Kane</b></figcaption>
        </div> <!-- left column -->
        <div class="col-md-6 middle">
          <form class="form-inline">
            <button class="btn btn-default center-block" type="submit">Compare!</button>
            <div class="form-group" id="gameweek">
              <label for="startTime">Game Week: </label>
              <select id="startTime" class="form-control sm-screen">
                <option value="1" selected>1</option>
                <option value="20">20</option>
              </select>&nbsp;&nbsp;TO&nbsp;&nbsp;
              <select id="endTime" class="form-control sm-screen">
                <option value="1" selected>1</option>
                <option value="30">30</option>
              </select>
              <button type="button" class="btn btn-default" id="more_options">
                <span class="sr-only">More options</span>
                <span class="glyphicon glyphicon-chevron-down"></span>
              </button>
              <button type="button" class="btn btn-default" id="update_graph">
                <span class="sr-only">Update graph</span>                
                <span class="glyphicon glyphicon-refresh"></span>
              </button>
            </div>
            <div class="attributes hidden">
              <div class="form-group">
                <label class="labels">Points</label>
                <label class="radio-inline">
                  <input type="radio" name="points" id="points" value="line"> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="points" id="points" value="bar"> Bar graph
                </label>
                <button type="button" class="btn btn-default btn-sm" aria-label="Remove attribute from graph">Toggle</button>
              </div>
              <div class="form-group">
                <label class="labels">Price</label>
                <label class="radio-inline">
                  <input type="radio" name="price" id="price" value="line"> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="price" id="price" value="bar"> Bar graph
                </label>
                <button type="button" class="btn btn-default btn-sm" aria-label="Remove attribute from graph">Toggle</button>
              </div>
              <div class="form-group">
                <label class="labels">Goals</label>
                <label class="radio-inline">
                  <input type="radio" name="goals" id="goals" value="line"> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="goals" id="goals" value="bar"> Bar graph
                </label>
                <button type="button" class="btn btn-default btn-sm" aria-label="Remove attribute from graph">Toggle</button>
              </div>
              <div class="form-group">
                <label class="labels">Assists</label>
                <label class="radio-inline">
                  <input type="radio" name="assists" id="assists" value="line"> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="assists" id="assists" value="bar"> Bar graph
                </label>
                <button type="button" class="btn btn-default btn-sm" aria-label="Remove attribute from graph">Toggle</button>
              </div>
              <div class="form-group">
                <label class="labels">Clean sheets</label>
                <label class="radio-inline">
                  <input type="radio" name="cleanSheets" id="cleanSheets" value="line"> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="cleanSheets" id="cleanSheets" value="bar"> Bar graph
                </label>
                <button type="button" class="btn btn-default btn-sm" aria-label="Remove attribute from graph">Toggle</button>
              </div>
            </div>
          </form>
          <table class="table table-bordered table-condensed">
            <caption class="help-block text-warning hidden">
              <span class="glyphicon glyphicon-alert"></span> Player not found!
            </caption>
            <thead>
              <tr class="thead-row-color">
                <th>Kane</th>
                <th>Attributes</th>
                <th>Vardy</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="values">10</td>
                <td>Points</td>
                <td class="values text-success bg-success">100</td>
              </tr>
              <tr>
                <td class="values">40%</td>
                <td>Selected by</td>
                <td class="values text-success bg-success">60%</td>
              </tr>
              <tr>
                <td class="values">£10.4M</td>
                <td>Price</td>
                <td class="values text-success bg-success">£7.9M</td>
              </tr>
              <tr>
                <td class="values text-success bg-success">19</td>
                <td>Goals</td>
                <td class="values">15</td>
              </tr>
              <tr>
                <td class="values">10</td>
                <td>Assists</td>
                <td class="values">100</td>
              </tr>
              <tr>
                <td class="values">10</td>
                <td>Clean sheets</td>
                <td class="values">100</td>
              </tr>
              <tr>
                <td class="values">10</td>
                <td>Yellow cards</td>
                <td class="values">100</td>
              </tr>
              <tr>
                <td class="values">No</td>
                <td>Suspended?</td>
                <td class="values">No</td>
              </tr>
            </tbody>
          </table>
        </div> <!-- middle column -->
        <div class="col-md-3 right">
          <div class="input-group">
            <input id="player2" class="form-control" name="player2" type="search">
            <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
          </div>
          <figure>
            <img src="faces/101668.jpg" class="img-responsive center-block" alt='Jamie Vardy'>
          </figure>
          <figcaption class="text-center"><b>Vardy</b></figcaption>
        </div> <!-- right column -->
      </div> <!-- end of first row! -->
      <div class="row">
        <div class="col-xs-12 graph_col">
          <div id="graph_container"></div>
        </div>
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
    <script src="js/unstick_buttons.js"></script>
    <script src="js/accent_map.js"></script>
    <script src="js/profile_helpers.js"></script>
    <script src="js/profile_searchbar.js"></script>
    <script type="text/javascript">
      var chart;
      $(document).ready(function() {
        centElement($('.form-group'));
        $(window).resize(function() {
            centElement($('.form-group')); 
        });
        $("#more_options").click(function() {
          $(".attributes").toggleClass("hidden");
          centElement($('.form-group'));
        });

        var searchBars = new PlayerSearchBar("#player1, #player2");
        $("button[type='submit']").click(function(e) {
          searchBars.onSearch(e, ["#player1", "#player2"]);
        });

        hideErrorPrompts("#player1, #player2");

        var initOptions = {
          chart: {
              renderTo: "graph_container",
              height: 350,
              width: 350
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
            pie: {
              tooltip: {
                headerFormat: '<b>{point.key}</b><br>',
                pointFormat: '<span>{point.percentage:.0f}%</span>'
              }
            },
            column: {
              stacking: "normal"
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
              layout: 'vertical',
              align: 'right',
              verticalAlign: 'middle',
              borderWidth: 0,
              enabled: false
          },
          series: [{
            name: 'Tokyo',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
          }],
          credits: {
              enabled: false //Removes the highchart.com label at bottom right of graph
          }
        };
        chart = new Highcharts.Chart(initOptions);
      });
    </script>
  </body>
</html>