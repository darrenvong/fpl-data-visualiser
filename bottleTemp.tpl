<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>{{name}}</title>
        <script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>
        <script>
            $(document).ready(function() {
                $('#j').text("This is some text from JavaScript! Yo!");
                console.log($('#players2').val());
            });
        </script>
    </head>
    <body>
        <p>Hello {{name}}</p>
        <p id="j"></p>

        <select id="players2" name="players2">
            <option value="Mahrez">Mahrez</option>
            <option value="Lukaku" selected>Lukaku286</option>
            <option value="Ozil">Ozil</option>
            <option value="Vardy">Vardy</option>
        </select>
    </body>
</html>