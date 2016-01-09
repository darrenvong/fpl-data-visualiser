<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>{{name}}</title>
        <script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>
        <script>
            $(document).ready(function() {
                $('#j').text("This is some text from JavaScript! Yo!");
            });
        </script>
    </head>
    <body>
    % for i in xrange(5):
        <p>{{name}}</p>
    % end
    <p id="j"></p>
    </body>
</html>