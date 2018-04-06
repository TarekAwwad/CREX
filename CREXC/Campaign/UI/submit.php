<?php
if ( parse_url($_SERVER['HTTP_REFERER'])['host'] !== 'project-crowd.eu' && realpath(__FILE__) === realpath( $_SERVER['SCRIPT_FILENAME'] ) ) {
    /*Header to send, 404 even if the files does exist for security */
    header( 'HTTP/1.0 404 Not Found', TRUE, 404 );
    die( header( 'location: ./error.php?msg=da' ) );
}
session_start();
$_SESSION["submitted"] = true;
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
</head>
<body>
<script src="./lib/generate_header.js"></script>
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
        <div id="profile_content" class="col-sm-11 list-group-item list-group-item-success message">
            <p>Thank you for your participation!</p>
            <p>In order to submit your contribution and get payed, please go back to Crowdflower and fill in the following code : <span class="nb"> <?php echo $_GET["scid"]?></span></p>
            <p>It is safe to close this window ONCE your contribution is validated on crowdflower </p>
        </div>
    </div>
</div>
<!-- FOOTER -->
<footer class="text-center">
    <p>Style modified and redistributed under the &copy; <a
                href="http://creativecommons.org/licenses/by/3.0/">CC-3.0</a> license. Original template <a
                href="https://evenfly.com">EvenFly </a>. </p>
</footer>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
<script src="./lib/jquery.nicescroll.min.js"></script>
<script src="./lib/evenfly.js"></script>
</body>
