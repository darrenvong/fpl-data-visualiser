<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="Multi-player comparator">
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
    <link href="css/multi_player.css" rel="stylesheet">

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
          <form>
            <div class="form-group">
              <label for="position">Position: </label>
              <select class="form-control" id="position">
                <option value="all">All</option>
                <option value="goalkeepers">Goalkeepers</option>
                <option value="defenders">Defenders</option>
                <option value="midfielders">Midfielders</option>
                <option value="forwards">Forwards</option>
              </select>
            </div>
            <div class="form-group">
              <label for="startTime">Game week: </label>
              <select id="startTime" class="form-control">
                <option value="1">1</option>
                <option value="38">38</option>
              </select>&nbsp;&nbsp;TO&nbsp;&nbsp;
              <select id="endTime" class="form-control">
                <option value="1">1</option>
                <option value="38">38</option>
              </select>
            </div>
            <div class="form-group filter-block">
              <label>Filter by: </label>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="points">Points
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="selectedBy">Selected By
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="form">Form
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="price">Price
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="goals">Goals
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="assists">Assists
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="minutesPlayed">Minutes Played
                </label>
              </div>
            </div>
            <div class="form-group">
              <button type="button" class="btn btn-default center-block">Update</button>
            </div>
          </form>
        </div> <!-- end of left column -->
        <div class="col-md-offset-1 col-md-8 right">
          <form class="form-inline" id="num_players">
            <div class="form-group">
              <label>Players on page: </label>
              <select class="form-control">
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
              </select>
            </div>
          </form>
          <div class="panes">
            <ul class="nav nav-tabs" role="tablist">
              <li role="presentation" class="active">
                <a href="#table" aria-controls="table_view" role="tab" data-toggle="tab">Table view</a>
              </li>
              <li role="presentation">
                <a href="#graph" aria-controls="graph_view" role="tab" data-toggle="tab">Graph view</a>
              </li>
            </ul>

            <div class="tab-content">
              <div role="tabpanel" class="tab-pane fade in active" id="table">
                <table class="table table-bordered">
                  <thead>
                    <tr class="thead-row-color">
                      <th>Rank</th>
                      <th>Name</th>
                      <th>Attribute</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="points">
                      <td>1</td>
                      <td>Mahrez</td>
                      <td>100</td>
                    </tr>
                    <tr id="points">
                      <td>2</td>
                      <td>Vardy</td>
                      <td>95</td>
                    </tr>
                    <tr id="points">
                      <td>3</td>
                      <td>Kane</td>
                      <td>93</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div role="tabpanel" class="tab-pane fade" id="graph">
                <div id="graph_container"></div>
              </div>            
            </div>
          </div>
        </div> <!-- end of right column -->
      </div> <!-- end of row -->

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
    <script src="js/math.min.js"></script>
    <script src="js/accent_map.js"></script>
    <script src="js/unstick_buttons.js"></script>
    <script src="js/helpers.js"></script>
    <script>
      $(function () {
        $('#graph_container').highcharts({
            title: {
                text: 'Monthly Average Temperature',
                x: -20 //center
            },
            subtitle: {
                text: 'Source: WorldClimate.com',
                x: -20
            },
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Temperature (°C)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: '°C'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Tokyo',
                data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
            }, {
                name: 'New York',
                data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
            }, {
                name: 'Berlin',
                data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
            }, {
                name: 'London',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
      });
    </script>
  </body>
</html>
