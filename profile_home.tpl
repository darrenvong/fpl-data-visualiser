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
    <link href="css/general.css" rel="stylesheet">
    <link href="css/profile.css" rel="stylesheet">

    <!-- New native Array API polyfill for IE by Mozilla Developer Network (2016)
    (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/) -->
    <!--[if IE]>
      <script src="js/array_polyfill.js"></script>
    <![endif]-->

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
        <div class="col-md-12 center-searchbar">
          <form method="post">
            <label for="player-names">Player's name: </label>
            <input id="player-names" class="form-control" name="player_name" type="search" size="30" placeholder="Type part of a player's name to begin">
            <button type="submit" class="btn btn-default large-searchbar-btn">
              <span class="sr-only">Search</span>
              <span class="glyphicon glyphicon-search"></span>
            </button>
            <p class="help-block text-warning hidden"><span class="glyphicon glyphicon-alert"></span> Player not found!</p>
          </form>
        </div> <!-- div.col-md-12 -->
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
    <script src="js/accent_map.js"></script>
    <script src="js/unstick_buttons.js"></script>
    <script src="js/profile_helpers.js"></script>
    <script src="js/profile_searchbar.js"></script>
    <!-- Main method script -->
    <script src="js/profile_home.js"></script>
  </body>
</html>