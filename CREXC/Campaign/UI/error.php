<?php
session_start();
?>

<!DOCTYPE html>
<html lang="">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- SITE TITLE -->
    <title>CrowdFlower - All question campaign</title>
    <!-- FAVICONS -->
    <link rel="icon" href="img/logo.png">
    <!-- STYLESHEETS -->
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/responsive.css">
    <!-- FONTS & ICONS -->
    <link href='//fonts.googleapis.com/css?family=Kristi|Alegreya+Sans:300' rel='stylesheet' type='text/css'>
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet"> </head>

<body>
    <script src="./lib/generate_header.js"></script>
    <script src="./lib/back_refresh_alert.js"></script>

    <div class="container">
        <!-- HEADER -->
        <div id="header" class="row">
            <script>
                create_header('header', "")
            </script>
        </div>
        <hr>
        <!-- Error Message -->
        <div class="col-sm-11">
            <div class="col-sm-1"></div>
            <div id="profile_content" class="col-sm-11 list-group-item list-group-item-danger"> Error:
                <?php
                    if($_GET["msg"] == "id") {echo "This contributor ID has been already used "; }
                    if($_GET["msg"] == "da") {echo "This page does not exist ";}
                    if($_GET["msg"] == "te") {echo "Task already submitted by current user";}
                ?>
            </div>
        </div>
    </div>
    <!-- FOOTER -->
    <footer class="text-center">
        <p>Style modified and redistributed under the &copy; <a href="http://creativecommons.org/licenses/by/3.0/">CC-3.0</a> license. Original template <a href="https://evenfly.com">EvenFly </a>. </p>
    </footer>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
    <script src="./lib/jquery.nicescroll.min.js"></script>
    <script src="./lib/evenfly.js"></script>
</body>

</html>