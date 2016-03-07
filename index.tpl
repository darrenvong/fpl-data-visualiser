<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="img/favicon.ico">

    <title>Fantasy Premier League player Data Visualiser</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

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
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li class="dropdown">
              <a href="#" id="tools-dd" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                Tools
                <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="profiles">Player profiles</a></li>
                <li><a href="#">Head-to-head comparator</a></li>
                <li><a href="#">Multi-player comparator</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main jumbotron -->
    <div class="jumbotron">
      <div class="container">
        <h1>FPL Player Data Visualiser</h1>
        <p>A set of tools which help you find top-notch players and boost your ranking in Fantasy Premier League!</p>
        <!-- <p><a class="btn btn-success btn-lg" href="#" role="button">Learn more &raquo;</a></p> -->
      </div>
    </div>

    <div class="container">
      <!-- Tables of the most wanted players -->
      <div class="row">
        % import home
        <div class="col-md-4">
          <h2>Hottest players</h2>
          <table class="table table-bordered">
            <thead>
              <tr class="thead-row-color">
                <th>Name</th>
                <th>Club</th>
                <th>Value</th>
                <th>Points</th>
                <th>Form Score</th>
              </tr>
            </thead>
            <tbody>
              {{ !home.generate_tables(hot_players, 8, table_type="hot_players") }}
            </tbody>
          </table>
        </div>
        <div class="col-md-4">
          <h2>Pound stretchers</h2>
          <table class="table table-bordered">
            <thead>
              <tr class="thead-row-color">
                <th>Name</th>
                <th>Club</th>
                <th>Value</th>
                <th>Points</th>
              </tr>
            </thead>
            <tbody>
              {{ !home.generate_tables(pound_stretchers, 8) }}
            </tbody>
          </table>
       </div>
        <div class="col-md-4">
          <h2>Most popular this week</h2>
          <table class="table table-bordered">
            <thead>
              <tr class="thead-row-color">
                <th>Name</th>
                <th>Club</th>
                <th>Value</th>
                <th>Points</th>
                <th>Net Transfer</th>
              </tr>
            </thead>
            <tbody>
              {{ !home.generate_tables(popular_players, 8, table_type="popular_players") }}
            </tbody>
          </table>
        </div>
      </div>

      <hr>

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
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
