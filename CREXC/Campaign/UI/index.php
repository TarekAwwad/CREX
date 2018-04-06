<?php
session_start();

if (isset($_SESSION["submitted"])) {
    if ($_SESSION["submitted"]) {
//        echo $_SESSION["submitted"];
               die(header('location: ./error.php?msg=da'));
    }
}

// Start the session

$t1 = date('h:i:sa');
$_SESSION["time_s"] = $t1;

$_SESSION["content"] = 'profile';
$_SESSION["scid"] = $_GET["id"];
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
<!-- Internal Dependencies -->
<script src="./res/profile.js"></script>
<script src="./res/description.js"></script>
<script src="./lib/generate_header.js"></script>
<script src="./lib/generate_dropdowns.js"></script>
<script src="./lib/generate_description.js"></script>
<script src="./lib/validate_inputs.js"></script>
<script src="./lib/back_refresh_alert.js"></script>

<!-- Main form -->
<form name="first_page" action="php/write_data.php" onsubmit="return !!(validateForm() && validateID())" method="post">
    <div class="container">
        <!-- HEADER -->
        <div id="header" class="row">
            <script>
                create_header('header', 'introduction')
            </script>
        </div>
        <hr>
        <!-- INTRODUCTION -->
        <div id="introduction" class="row mobmid">
            <script>
                create_desc('introduction', general_description_data)
            </script>
        </div>
        <hr>
        <!-- CONTRIBUTOR ID -->
        <div id="contributorID" class="row mobmid">
            <div class="col-sm-1"><span class="secicon fa fa-hand-pointer-o"></span></div>
            <!--icon end-->
            <div class="col-sm-11">
                <h3>Before you start</h3>
                <div class="row">
                    <div class="col-md-6">
                        <h4>Please fill in your contributor ID <a data-toggle="collapse" data-target="#abs1"
                                                                  class="more">Why?</a><br/></h4>
                        <div id="abs1" class="collapse abstract">
                            <p>This allows us to pay you the reward and eventually the bonus.</p>
                        </div>
                        <br/></div>
                </div>
                <div class="col-sm-1"></div>
                <div class="col-sm-9 list-group-item">
                    <div><span class="fa fa-angle-right"></span> Your contributor ID
                        <input name="cid" size="30" type="text" class="pull-right"> <span id="error_cid"
                                                                                          class="nb"></span></div>
                    <br>
                    <div><span class="fa fa-angle-right"></span> Confirm your contributor ID
                        <input name="ccid" size="30" type="text" class="pull-right"> <span id="error_ccid"
                                                                                           class="nb"></span></div>
                </div>
            </div>
        </div>
        <hr>
        <!-- PROFILE -->
        <div id="profile" class="row mobmid">
            <div class="col-sm-1"><span class="secicon fa fa-user"></span></div>
            <!--icon end-->
            <div class="col-sm-11">
                <h3>Your Profile</h3>
                <div class="row">
                    <div class="col-md-9">
                        <h4>Please fill in your profile in the fields below <a data-toggle="collapse"
                                                                               data-target="#abs2" class="more">Why?</a><br/>
                        </h4>
                        <div id="abs2" class="collapse abstract">
                            <p>Knowing some information about you is important for our research. <span class="nb"> Your data are anonymised</span>
                            </p>
                        </div>
                    </div>
                </div>
                <br/>
                <div class="col-sm-1"></div>
                <div id="profile_content" class="col-sm-9 list-group-item">
                    <script>
                        create_ddl('profile_content', profile_data)
                    </script>
                </div>
            </div>
        </div>
        <hr>
        <!-- SUBMIT -->
        <div id="validate" class="col-sm-11 text-right dl-share">
            <input id="val" class="a2a_dd btn list-group-item-custom" name="submit" type="submit" value="Start"
                   onclick="removeBackRefreshAlert()"/></div>
    </div>
</form>
<!-- FOOTER -->
<footer class="text-center">
    <p>Style modified and redistributed under the &copy; <a
                href="http://creativecommons.org/licenses/by/3.0/">CC-3.0</a> license. Original template <a
                href="https://evenfly.com">EvenFly </a>. </p>
</footer>
<!-- External Dependencies -->
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
<script src="./lib/jquery.nicescroll.min.js"></script>
<script src="./lib/evenfly.js"></script>
</body>

</html>