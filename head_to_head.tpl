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
    % import head_to_head
    % import general
    {{ !general.get_navbar() }}

    <!-- Main "body" of the page -->
    <div class="container profile-body">
      <div class="row">
        <div class="col-md-3 left">
          <form method="post" id="player1_field">
            <div class="input-group">
              <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
              <input id="player1" class="form-control" name="player1" type="search">
              <input type="hidden" class="player2_alias" name="player2">
            </div>
          </form>
          <figure>
            <img src={{u"faces/"+p1_profile['photo']}} class="img-responsive center-block" alt='{{p1_profile["normalised_name"]}}'>
          </figure>
          <figcaption class="text-center"><b>{{p1_profile["web_name"]}}</b></figcaption>
        </div> <!-- left column -->
        <div class="col-md-6 middle">
          <form class="form-inline" method="post">
            <button class="btn btn-default center-block" type="submit">Compare!</button>
            <p class="help-block text-warning hidden">
              <span class="glyphicon glyphicon-alert"></span> Player not found!
            </p>
            <input type="hidden" class="player1_alias" name="player1">
            <input type="hidden" class="player2_alias" name="player2">
            <div class="form-group" id="gameweek">
              <label for="startTime">Game Week: </label>
              <select id="startTime" class="form-control sm-screen">
                % start_gw = min(p1_profile["start_gw"], p2_profile["start_gw"])
                % latest_gw = int(max(p1_profile["current_gw"], p2_profile["current_gw"]))
                % for week in xrange(start_gw, latest_gw+1):
                <option value={{week}}>{{week}}</option>
                % end
              </select>&nbsp;&nbsp;TO&nbsp;&nbsp;
              <select id="endTime" class="form-control sm-screen">
                % for week in xrange(start_gw, latest_gw+1):
                  % if week == latest_gw:
                  <option value={{week}} selected>{{week}}</option>
                  % else:
                  <option value={{week}}>{{week}}</option>
                  % end
                % end
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
              <div class="form-group" id="points">
                <label class="labels">Points</label>
                <label class="radio-inline">
                  <input type="radio" name="points" class="points" value="line" checked> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="points" class="points" value="bar"> Bar graph
                </label>
                <label class="radio-inline last">
                  <input type="radio" name="points" class="points" value="box"> Box plot
                </label>
                <label class="checkbox-inline">
                  <input type="checkbox" class="points_switch" value="on" aria-label="Hides the 'points' attribute from graph"> Active
                </label>
                <a role="button" class="btn" data-toggle="popover" title="Points" data-content="Lorem ipsum..." data-trigger="hover" data-placement="right"><span class="glyphicon glyphicon-info-sign"></span></a>
              </div>
              <div class="form-group" id="goals">
                <label class="labels">Goals</label>
                <label class="radio-inline">
                  <input type="radio" name="goals" class="goals" value="line" checked> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="goals" class="goals" value="bar"> Bar graph
                </label>
                <label class="checkbox-inline">
                  <input type="checkbox" class="goals_switch" value="on" aria-label="Hides the 'goals' attribute from graph"> Active
                </label>
                <a role="button" class="btn" data-toggle="popover" title="Goals" data-content="Lorem ipsum..." data-trigger="hover" data-placement="right"><span class="glyphicon glyphicon-info-sign"></span></a>
              </div>
              <div class="form-group" id="assists">
                <label class="labels">Assists</label>
                <label class="radio-inline">
                  <input type="radio" name="assists" class="assists" value="line" checked> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="assists" class="assists" value="bar"> Bar graph
                </label>
                <label class="checkbox-inline">
                  <input type="checkbox" class="assists_switch" value="on" aria-label="Hides the 'assists' attribute from graph"> Active
                </label>
                <a role="button" class="btn" data-toggle="popover" title="Assists" data-content="Lorem ipsum..." data-trigger="hover" data-placement="right"><span class="glyphicon glyphicon-info-sign"></span></a>
              </div>
              <div class="form-group" id="cleanSheets">
                <label class="labels">Clean sheets</label>
                <label class="radio-inline">
                  <input type="radio" name="cleanSheets" class="cleanSheets" value="line" checked> Line graph
                </label>
                <label class="radio-inline bar">
                  <input type="radio" name="cleanSheets" class="cleanSheets" value="bar"> Bar graph
                </label>
                <label class="checkbox-inline">
                  <input type="checkbox" class="cleanSheets_switch" value="on" aria-label="Hides the 'clean sheets' attribute from graph"> Active
                </label>
                <a role="button" class="btn" data-toggle="popover" title="Clean sheets" data-content="Lorem ipsum..." data-trigger="hover" data-placement="right"><span class="glyphicon glyphicon-info-sign"></span></a>
              </div>
            </div>
          </form>
          <div class="alert alert-danger hidden" role="alert"><span class="glyphicon glyphicon-alert"></span>
            &nbsp;&nbsp;When "Box plot" is selected and the "Active" box of <b>Points</b> is checked, other "Active" boxes cannot be checked. Please either uncheck all of the other "Active" boxes, or deselect "Box plot" from <b>Points</b> to continue.
          </div>
          <div id="graph_container"></div>
        </div> <!-- middle column -->
        <div class="col-md-3 right">
          <form method="post" id="player2_field">
            <div class="input-group">
              <input id="player2" class="form-control" name="player2" type="search">
              <input type="hidden" class="player1_alias" name="player1">
              <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
            </div>
          </form>
          <figure>
            <img src={{u"faces/"+p2_profile['photo']}} class="img-responsive center-block" alt='{{p2_profile["normalised_name"]}}'>
          </figure>
          <figcaption class="text-center"><b>{{p2_profile["web_name"]}}</b></figcaption>
        </div> <!-- right column -->
      </div> <!-- end of first row! -->
      <div class="row">
        <div class="col-xs-offset-3 col-xs-6">
          <table class="table table-bordered table-condensed">
            <thead>
              <tr class="thead-row-color">
                <th>{{p1_profile["web_name"]}}</th>
                <th>Attributes</th>
                <th>{{p2_profile["web_name"]}}</th>
              </tr>
            </thead>
            <tbody>
              {{ !head_to_head.generate_table(p1_profile, p2_profile) }}
              <tr id="available">
                <td class="values {{' text-success bg-success' if p1_profile['status'] == 'a' and p2_profile['status'] != 'a' else ''}}">
                  {{"Yes" if p1_profile["status"] == 'a' else "No"}}
                </td>
                <td>Available?</td>
                <td class="values {{' text-success bg-success' if p2_profile['status'] == 'a' and p1_profile['status'] != 'a' else ''}}">
                  {{"Yes" if p2_profile["status"] == 'a' else "No"}}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="col-xs-3"></div>
      </div>

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
    <script src="js/highcharts.js"></script>
    <script src="js/highcharts-more.js"></script>
    <script src="js/unstick_buttons.js"></script>
    <script src="js/accent_map.js"></script>
    <script src="js/helpers.js"></script>
    <script src="js/profile_searchbar.js"></script>
    <!-- // <script src="js/profile_graph.js"></script> -->
    <script src="js/head_to_head_graph.js"></script>
    <script src="js/head_to_head.js"></script>
  </body>
</html>