<!doctype html>
<html id="html">
    <head>
        <title>GradeMan School Manager</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" type="text/css" href="{{ relroot }}static/main.css" />
        <script>
            function printView() {
                document.getElementById('html').style.fontSize = '16px';
                document.getElementById('html').style.backgroundColor = '#aaa';
                document.getElementById('body').style.width = '21.0cm';
                document.getElementById('body').style.paddingRight = '1.5cm';
                document.getElementById('body').style.paddingLeft = '1.5cm';
                document.getElementById('nav').style.display = 'none';
                var noPrint = document.getElementsByClassName('no-print');
                for(var i=0, len=noPrint.length; i<len; i++) {
                    noPrint[i].style.display = 'none';
                }
            }
        </script>
    </head>
    <body id="body">
        {{ nav }}
        {{ content }}
    </body>
</html>
