<?php
if (parse_url($_SERVER['HTTP_REFERER'])['host'] !== 'project-crowd.eu' && realpath(__FILE__) === realpath($_SERVER['SCRIPT_FILENAME'])) {
    /*Header to send, 404 even if the files does exist for security */
    header('HTTP/1.0 404 Not Found', TRUE, 404);
//        TODO: Check this condition
    /* choose the appropriate page to redirect users */
    die(header('location: ./error.php?msg=da'));

}

session_start();
if ($_SESSION["submitted"]) {
    die(header('location: ./error.php?msg=da'));
}

if (!isset($_SESSION["cid"])) {
    die(header('location: ./error.php?msg=da'));
}


$t1 = date('h:i:sa');
$_SESSION["time_s"] = $t1;

$_SESSION["content"] = 'task';
$_SESSION["tid"] = $_SESSION['version'][$_SESSION['next']];
?>
<!DOCTYPE html>
<html lang="">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- SITE TITLE -->
    <title>ProjecCrowd</title>
    <!-- FAVICONS -->
    <link rel="icon" href="img/logo.png">
    <!-- STYLESHEETS -->
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/responsive.css">
    <!-- FONTS & ICONS -->
    <link href='//fonts.googleapis.com/css?family=Kristi|Alegreya+Sans:300' rel='stylesheet' type='text/css'>
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script>
        (function (i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r;
            i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date();
            a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
            a.async = 1;
            a.src = g;
            m.parentNode.insertBefore(a, m)
        })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

        ga('create', 'UA-109211482-1', 'auto');
        ga('send', 'pageview');
    </script>
</head>

<body>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<!-- Internal Dependencies -->
<?php
echo '<script src="./res/task_' . $_SESSION["tid"] . '_desc.js"></script>';
echo '<script src="./res/task_' . $_SESSION["tid"] . '_auto.js"></script>';
?>

<script src="./lib/generate_header.js"></script>
<script src="./lib/generate_description.js"></script>
<script src="./lib/generate_task.js"></script>
<script src="./lib/validate_inputs.js"></script>
<script src="./lib/back_refresh_alert.js"></script>

<!-- Main form -->
<form name="first_page" action="php/write_data.php" onsubmit="return validateForm()" method="post">
    <div class="container">
        <!-- HEADER -->
        <div id="header" class="row">
            <script>
                create_header("header", "")
            </script>
        </div>
        <hr>
        <!-- INTRODUCTION -->
        <div id="introduction" class="row mobmid">
            <script>
                create_desc('introduction', task_description_data)
            </script>
        </div>

        <hr>
        <!-- TASK -->
        <div id="task" class="row mobmid">
            <div class="col-sm-1"><span class="secicon fa fa-user"></span></div>
            <div id="hits" class="col-sm-11">
                <h3>The Task</h3>
                <br>
                <script>
                    create_task('hits', task_data)
                </script>
            </div>
        </div>
        <hr>

        <div id="taskco" class="row mobmid">
            <div class="col-sm-1"><span class="secicon fa fa-lightbulb-o"></span></div>

            <div class="col-sm-11">
                <div class="col-md-12 list-group-item">
                    <div class="col-md-1"></div>
                    <div class="col-md-10"></div>
                    <div class="col-md-1"></div>
                    <span class="nb" id="error_codec"></span>
                    <div class="hit-content-text-op">
                        Please copy the following code to the field <?php echo '<span class="nbCap">' . $_SESSION["tid"] . "</span>" ?> on the
                        Crowdflower task page: <?php echo '<span class="nbCap">' . rand(100, 999) . "</span>"?><br>
                        <input type="checkbox" name="codec" id="codec" value="0"> Code copied? Now check this box and hit Next Step.
                    </div>

                </div>
            </div>
        </div>
        <hr>
        <!-- SUBMIT -->
        <div id="validate" class="col-sm-11 text-right dl-share">
            <input id="val" class="a2a_dd btn list-group-item-custom" type="submit" name="submit" value="Next step"
                   onclick="removeBackRefreshAlert()"/></div>
    </div>
</form>
<!-- FOOTER -->
<footer class="text-center">
    <p>Style modified and redistributed under the &copy; <a
                href="http://creativecommons.org/licenses/by/3.0/">CC-3.0</a> license. Original template <a
                href="https://evenfly.com">EvenFly </a>. </p>
</footer>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
<script src="./lib/jquery.nicescroll.min.js"></script>
<script src="./lib/evenfly.js"></script>
</body>

</html>