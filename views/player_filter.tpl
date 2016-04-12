<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="Multi-attribute player filter">
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
    <link href="css/player_filter.css" rel="stylesheet">

    <!-- Polyfill fixes by Mozilla Developer Network (2016), https://developer.mozilla.org/ -->
    <script src="js/polyfills.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    % from views import general, player_filter, helpers
    % VALUE_TO_DATA_KEY = player_filter.VALUE_TO_DATA_KEY
    {{ !general.get_navbar() }}
    

    <!-- Main "body" of the page -->
    <div class="container profile-body">
      <div class="row">
        <div class="col-md-3 left">
          <form method="post">
            <div class="form-group">
              <label for="position">Position: </label>
              <select class="form-control" id="position" name="position">
                {{!player_filter.get_previous_position_state(position)}}
              </select>
            </div>
            <div class="form-group">
              <label for="startTime">Game week: </label>
              <select id="startTime" class="form-control" name="start">
                % for gw in xrange(1, current_gw+1):
                  % if gw == int(start):
                    <option value={{gw}} selected>{{gw}}</option>
                  % else:
                    <option value={{gw}}>{{gw}}</option>
                  % end
                % end
              </select>&nbsp;&nbsp;TO&nbsp;&nbsp;
              <select id="endTime" class="form-control" name="end">
                % for gw in xrange(1, current_gw+1):
                  % if gw == int(end): 
                    <option value={{gw}} selected>{{gw}}</option>
                  % else:
                    <option value={{gw}}>{{gw}}</option>
                  % end
                % end
              </select>
            </div>
            <span class="help-block">Notes: the "Game week" range has an effect on <b>Points</b>, <b>Goals</b>, <b>Assists</b>, <b>Clean sheets</b> and <b>Minutes played</b> only.</span>
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
                  <input type="checkbox" value="on" name="form">Form
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="selectedBy">Selected by
                </label>
              </div>
              <div class="checkbox hidden cs">
                <label>
                  <input type="checkbox" value="on" name="cleanSheets">Clean sheets
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
                  <input type="checkbox" value="on" name="price">Price
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="netTransfers">Net transfers
                </label>
              </div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" value="on" name="minutesPlayed">Minutes played
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
              <span class="num_players_label">Top 
                <select class="form-control" id="num_players">
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                </select>
                players
              </span>
            </div>
          </form>
          <div class="ranked_table">
            <table class="table table-bordered">
              <thead>
                <tr class="thead-row-color">
                  <th>Rank</th>
                  <th>Name</th>
                  <th>Club</th>
                  % if "position" in player_stats[0]:
                  <th>Position</th>
                  % end
                  % for sf in selected_filters:
                  <th>{{helpers.capitalise_camel_case_words(sf)}}</th>
                  % end
                </tr>
              </thead>
              <tbody>
                % for counter, player in enumerate(player_stats, start=1):
                  <tr>
                    <td>{{counter}}</td>
                    <td>{{player["web_name"]}}</td>
                    <td>{{player["team_name"]}}</td>
                  % if "position" in player:
                    <td>{{player["position"]}}</td>
                  % end
                  % for sf in selected_filters:
                    % if sf == "selectedBy":
                      <td>{{player[VALUE_TO_DATA_KEY[sf]]}}%</td>
                    % elif sf == "price":
                      <td>£{{player[VALUE_TO_DATA_KEY[sf]]/10.0}}M</td>
                    % else:
                      <td>{{player[VALUE_TO_DATA_KEY[sf]]}}</td>
                    % end
                  % end
                % end
              </tbody>
            </table>           
          </div>
        </div> <!-- end of right column -->
      </div> <!-- end of row -->

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
    <script src="js/math.min.js"></script>
    <script src="js/accent_map.js"></script>
    <script src="js/unstick_buttons.js"></script>
    <script src="js/helpers.js"></script>
    <script src="js/player_filter.js"></script>
  </body>
</html>
