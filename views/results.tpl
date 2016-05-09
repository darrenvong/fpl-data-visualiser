<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="Stat analysis">
    <meta name="author" content="Darren Vong">
    <link rel="icon" href="img/favicon.ico">

    <title>Fantasy Premier League player Data Visualiser</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/general.css" rel="stylesheet">

    <!-- Polyfill fixes by Mozilla Developer Network (2016), https://developer.mozilla.org/ -->
    <script src="js/min/polyfills.min.js"></script>
    
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    % from views import general
    {{!general.get_navbar()}}
    <div class="container profile-body">
      <!-- tabs -->
      <ul class="nav nav-tabs" role="tablist">
        <li role="presentation" class="active">
          <a href="#survey_graph" aria-controls="survey_graph" role="tab" data-toggle="tab">Usefulness</a>
        </li>
        <li role="presentation">
          <a href="#survey_graph2" aria-controls="survey_graph2" role="tab" data-toggle="tab">Navigability</a>
        </li>
      </ul>

      <!-- panes -->
      <div class="tab-content">
        <div role="tabpanel" class="tab-pane fade in active" id="survey_graph" style="padding-top: 10px;"></div>
        <div role="tabpanel" class="tab-pane fade" id="survey_graph2" style="padding-top: 10px;"></div>
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
    <script src="js/highcharts.js"></script>
    <script src="js/highcharts-more.js"></script>
    <script src="js/modules/exporting.js"></script>
    <script src="js/min/unstick_buttons.min.js"></script>
    <script>
      $(function() {
        var initOptions = {
          colors: ['#f5882b', '#7cb5ec', '#8085e9', '#6ae750',
                    '#f15c80'],
          chart: {
            renderTo: "survey_graph",
            style: {
              "fontFamily": 'Arial, Helvetica, sans-serif', // default font
              "fontSize": '12px',
              "-webkit-font-smoothing": "antialiased"
            }
          },
          title: {
            text: ('To what extent do you agree with the following: I find the available graphs '+
              'in the application more useful than the "Statistics" page on the FPL website.')
          },
          tooltip: {
              followPointer: true,
          },
          legend: {
              align: 'right',
              verticalAlign: 'bottom',
              borderWidth: 0,
              itemStyle: {"color": "#333333", "cursor": "pointer", "fontSize": "24px", "fontWeight": "bold" }
          },
          plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
          },
          legend: {
            align: 'right',
            layout: 'vertical',
            verticalAlign: 'middle',
            borderWidth: 0
          },
          series: [{
            data: [{
              name: "1 - Strongly Disagree",
              y: 0
            }, {
              name: "2 - Disagree",
              y: 1
            }, {
              name: "3 - Neither Agree or Disagree",
              y: 0
            },{
              name: "4 - Agree",
              y: 4
            }, {
              name: "5 - Strongly Agree",
              y: 0
            }],
            type: "pie",
            dataLabels: {
              enabled: true,
              distance: -50,
              formatter: function() {return (this.percentage) ? Math.round(this.percentage)+"%" : "";},
              style: {"color": "white", "fontSize": "16px", "fontWeight": "bold", "textShadow": "none"}
            }
          }],
          credits: {
              enabled: false //Removes the highchart.com label at bottom right of graph
          }
        };
        new Highcharts.Chart(initOptions);

        // Option alterations for the second graph
        initOptions.chart.renderTo = "survey_graph2";
        initOptions.title.text = 'How hard was it to navigate around the website?';
        initOptions.series[0].data = [{
            name: "1 - Very Hard",
            y: 0
          }, {
            name: "2 - Hard",
            y: 1
          }, {
            name: "3 - Neither Easy or Hard",
            y: 0
          }, {
            name: "4 - Easy",
            y: 6
          }, {
            name: "5 - Very Easy",
            y: 6
          }];
        new Highcharts.Chart(initOptions);
      });
    </script>
  </body>
</html>
