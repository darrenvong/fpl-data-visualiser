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

    % from views import general
    {{ !general.get_navbar() }}

    <!-- Main "body" of the page -->
    <div class="container profile-body">
      <div class="row">
        <div class="col-md-3 left">
          <form method="post" id="player1_field">
            <div class="input-group">
              <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
              <input id="player1" class="form-control" name="player1" type="search">
              <input class="player2_alias" name="player2" type="hidden">
            </div>
          </form>
        </div> <!-- left column -->
        <div class="col-md-6 middle">
          <form method="post" id="neutral">
            <input type="hidden" class="player1_alias" name="player1">
            <input type="hidden" class="player2_alias" name="player2">
            <button id="home_compare_btn" class="btn btn-default center-block" type="submit">Compare!</button>
            <p class="help-block text-warning profile-page hidden"><span class="glyphicon glyphicon-alert"></span> Player not found!</p>
          </form>
        </div> <!-- middle column -->
        <div class="col-md-3 right">
          <form method="post" id="player2_field">
            <div class="input-group">
              <input id="player2" class="form-control" name="player2" type="search">
              <input class="player1_alias" name="player1" type="hidden">
              <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
            </div>
          </form>
        </div> <!-- right column -->
      </div> <!-- END of 1st row -->

      {{!general.get_footer()}}
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
    <script src="js/unstick_buttons.js"></script>
    <script src="js/accent_map.js"></script>
    <script src="js/helpers.js"></script>
    <script src="js/profile_searchbar.js"></script>
    <script src="js/h2h_home.js"></script>
  </body>
</html>