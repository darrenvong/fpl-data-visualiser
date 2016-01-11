<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>{{name}}</title>
        <script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>
        <script>
            $(document).ready(function() {
                $('#j').text("This is some text from JavaScript! Yo!");
                $('#clicky').on("click", function() {
                    $.post("/secret", function(data) {
                        console.log(data);
                    });
                });
            });
        </script>
    </head>
    <body>
        <p>Hello {{name}}</p>
        <p id="j"></p>
        <select id="players" name="players">
            <option value="Lukaku" selected>Lukaku</option>
            <option value="Vardy">Vardy</option>
            <option value="Mahrez">Mahrez</option>
            <option value="Kante">Kante</option>
        </select>
        <button id="clicky">Let's Go!</button>
    </body>
</html>