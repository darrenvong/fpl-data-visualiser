<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Highcharts Example</title>

		<script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>
		<style type="text/css">
${demo.css}
		</style>
        <script src="js/highcharts.js"></script>
        <script src="js/highcharts-more.js"></script>
        <script src="js/modules/exporting.js"></script>
        <script src="js/math.min.js"></script>
	</head>
	<body>
        <label for="players">Player's name:</label>
        <select id="players" name="players">
            % for player in playData:
            <option value={{player}}>{{player if player.count("_")==0 else player.replace("_", " ")}}</option>
            % end
        </select>
        <button id="drawline">Draw line</button>


        <button id="drawbox">Draw box</button><br>
        <label for="players2">Player 2's name:</label>
        <select id="players2" name="players2">
            % for player in playData:
            <option value={{player}}>{{player if player.count("_")==0 else player.replace("_", " ")}}</option>
            % end
        </select>
        <button id="correlate">Correlate players!</button>
    <div id="container" style="min-width: 310px; margin: 0 auto"></div>

	</body>
    <script type="text/javascript" src="js/fpl_graphs.js"></script>
</html>
