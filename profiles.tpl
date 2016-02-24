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
    <link rel="stylesheet" href="css/jquery-ui.theme.min.css">
    <link rel="stylesheet" href="css/jquery-ui.structure.min.css">

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
        <div class="col-md-6">
          <label for="player-names">Player's name: </label>
          <input id="player-names" type="text" size="20">
          <button type="button" class="btn btn-default">
            <span class="sr-only">Search</span>
            <span class="glyphicon glyphicon-search"></span>
          </button>
          <figure>
            <img src="img/Mahrez.jpg" class="img-responsive center-block" alt="Mahrez">
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
        <div class="col-md-6">
          <!-- <div class="dropdown">
            <button id="performance-metric" class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true">
              <span class="caret pull-right"></span>
            </button>
            <ul class="dropdown-menu">
              <li><a href="#">Consistency</a></li>
              <li><a href="">Mean score</a></li>
              <li><a href="">Cumulative total</a></li>
            </ul>
          </div> -->
          <div class="row">
            <div class="col-md-4">
              <p><b>Performance metric:</b></p>
              <select>
                <option value="1">Consistency</option>
                <option value="2">Mean Score</option>
                <option value="3">Cumulative Total</option>
              </select>
            </div>
            <div class="col-md-8">
              <p><b>Time:</b></p>
              <select>
                <option value="x">Between</option>
              </select>
              <span id="time-frame-input">
                <input type="text" size="5"> AND 
                <input type="text" size="5">
              </span>
            </div>
          </div>
            <figure>
              <img src="img/Mahrez_stats.jpeg" width="500" height="500">
            </figure>
        </div> <!-- end of col-md-6 (aka the right column) -->
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
    <script>
      var player_names = ["Mahrez", "Vardy", "Kane", "Sánchez"];
      $("#player-names").autocomplete({
        source: player_names,
        minLength: 0
      });
    </script>
  </body>
</html>
