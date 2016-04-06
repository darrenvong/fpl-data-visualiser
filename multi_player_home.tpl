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
          <form method="post">
            <div class="form-group">
              <label for="position">Position: </label>
              <select class="form-control" id="position" name="position">
                <option value="all">All</option>
                <option value="Goalkeeper">Goalkeepers</option>
                <option value="Defender">Defenders</option>
                <option value="Midfielder">Midfielders</option>
                <option value="Forward">Forwards</option>
              </select>
            </div>
            <div class="form-group">
              <label for="startTime">Game week: </label>
              <select id="startTime" class="form-control" name="start">
                % for gw in xrange(1, current_gw+1):
                <option value={{gw}}>{{gw}}</option>
                % end
              </select>&nbsp;&nbsp;TO&nbsp;&nbsp;
              <select id="endTime" class="form-control" name="end">
                % for gw in xrange(1, current_gw+1):
                  % if gw == current_gw: 
                <option value={{gw}} selected>{{gw}}</option>
                  % else:
                <option value={{gw}}>{{gw}}</option>
                  % end
                % end
              </select>
            </div>
            <span class="help-block">Notes: the "Game week" range has an effect on <b>Points</b> only.</span>
            <span class="help-block">The sort order of importance is the order in which the attributes are listed below, reading from top to bottom.</span>
            <div class="form-group filter-block">
              <label>Sort by: </label>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="points">Points
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="selectedBy">Selected By
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="form">Form
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="price">Price
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="goals">Goals
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="assists">Assists
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="netTransfers">Net Transfers
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="minutesPlayed">Minutes Played
                </label>
              </div>
            </div>
            <input type="hidden" class="num_players_alias" name="num_players">
            <div class="form-group">
              <button type="submit" class="btn btn-default center-block" id="update">Update</button>
            </div>
          </form>
        </div> <!-- end of left column -->
        <div class="col-md-offset-1 col-md-8 right">
          <form class="form-inline players_on_page">
            <div class="form-group">
              <label>Players on page: </label>
              <select class="form-control" id="num_players">
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
              </select>
            </div>
          </form>
          <div class="ranked_table">
            <table class="table table-bordered">
              <thead>
                <tr class="thead-row-color">
                </tr>
              </thead>
              <tbody>
              </tbody>
            </table>           
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
    <script src="js/multi_player.js"></script>
  </body>
</html>
