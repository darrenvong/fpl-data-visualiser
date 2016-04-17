<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="Home page">
    <meta name="author" content="Darren Vong">
    <link rel="icon" href="img/favicon.ico">

    <title>Fantasy Premier League player Data Visualiser</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/general.css" rel="stylesheet">
    <link href="css/home.css" rel="stylesheet">

    <!-- Polyfill fixes by Mozilla Developer Network (2016), https://developer.mozilla.org/ -->
    <script src="js/min/polyfills.min.js"></script>
    
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    % from views import general, home
    {{ !general.get_navbar() }}

    <!-- Main jumbotron -->
    <div class="jumbotron">
      <div class="container">
        <h1>FPL Player Data Visualiser</h1>
        <p>A set of tools to help you find the top-notch players and boost your ranking in Fantasy Premier League!</p>
        <!-- <p><a class="btn btn-success btn-lg" href="#" role="button">Learn more &raquo;</a></p> -->
      </div>
    </div>

    <div class="container">
      <!-- Tables of the most wanted players -->
      <div class="row">
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
              {{ !home.generate_tables(hot_players, table_type="hot_players") }}
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
              {{ !home.generate_tables(pound_stretchers) }}
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
              {{ !home.generate_tables(popular_players, table_type="popular_players") }}
            </tbody>
          </table>
        </div>
      </div>

      {{!general.get_footer()}}
    </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="js/jquery-2.1.4.min.js"><\/script>')</script>
    <script src="js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
    <script src="js/min/unstick_buttons.min.js"></script>
  </body>
</html>
