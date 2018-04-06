<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST' && realpath(__FILE__) === realpath($_SERVER['SCRIPT_FILENAME'])) {
    header('HTTP/1.0 404', TRUE, 404);
    die(header('location: ../error.php?msg=da'));
}

session_start();
if ($_SESSION["submitted"]) {
    die(header('location: ./error.php?msg=da'));
}

$t1 = strtotime($_SESSION["time_s"]);
$t2 = strtotime(date('h:i:sa'));
$elapsed_time = $t2 - $t1;

$fields = [];
$types = "";
$placeholders = [];

// Fetch data fields from POST
foreach ($_POST as $key => $value) {
    if (htmlspecialchars($key) !== 'ccid' && htmlspecialchars($key) !== 'submit') {
        array_push($fields, htmlspecialchars($key));
        $types = $types . 's';
        array_push($placeholders, '?');
    }
}

require_once("../../PrivateConfig/config.php");

// Connection to database
$mysqli = new mysqli($wgDBserver, $wgDBuser, $wgDBpassword, $wgDBname);

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}

if ($_SESSION["content"] == 'profile') {

    $_SESSION["cid"] = $_POST["cid"];

    //    Order of tasks appearance
    $task_order = array("go", "so", "de", "bi" , "fo", "ch", "a9", "sm", "us", "po", "a8");
//    $task_order = array("us");
    shuffle($task_order);
    $_SESSION["version"] = $task_order;
    $_SESSION["next"] = 0;

    //    Fetch data from POST
    $data = [];
    foreach ($fields as $field) {
        array_push($data, $_POST[$field]);
    }

    array_push($fields, "Version");
    array_push($fields, "Anchor");
    array_push($fields, "Elapsed");

    array_push($data, "'" . implode(',', $_SESSION["version"]) . "'");
    array_push($data, $_SESSION["next"]);
    array_push($data, $elapsed_time);

    array_push($placeholders, '?');
    array_push($placeholders, '?');
    array_push($placeholders, '?');

    $types = $types . 'ssi';

    // Prepared statement, stage 1: prepare 
    if (!($stmt = $mysqli->prepare("INSERT INTO contributor (" . implode(',', $fields) . ") VALUES (" . implode(',', $placeholders) . ")"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    //   Parameters to bind : types and data
    $param = [];
    array_push($param, $types);
    foreach ($data as $data_) {
        array_push($param, $data_);
    }

    //   Call_user_func_array takes object references
    $refs = array();
    foreach ($param as $key => $value) {
        $refs[$key] = &$param[$key];
    }

    //  Prepared statement, stage 2: bind and execute 
    if (!call_user_func_array(array($stmt, 'bind_param'), $refs)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    if (!$stmt->execute()) {
        if ($stmt->errno == 1062) {
            die(header('location: ../error.php?msg=id'));
        }
    }
    $stmt->close();
}

if ($_SESSION["content"] == 'task') {
    //   Insert the contribution into the database
    //   Prepared statement, stage 1: prepare
    if (!($stmt = $mysqli->prepare("INSERT INTO contribution (ID, TaskID, WorkerID, Content, Elapsed) VALUES (?, ?, ?, ?, ?)"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    $contribution_content = "{";

    foreach ($fields as $field) {
        $contribution_content = $contribution_content . $field . ':' . $_POST[$field] . ',';
    }
    $contribution_content = $contribution_content . "}";

    $tid = $_SESSION["tid"];
    $cid = $_SESSION["cid"];
    $uid = 'unit-' . $tid . '-' . $cid;

    //  Prepared statement, stage 2: bind and execute 
    if (!$stmt->bind_param('ssssi', $uid, $tid, $cid, $contribution_content, $elapsed_time)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    //    Update contribution anchor for the current contributor
    if (!($stmt = $mysqli->prepare("UPDATE contributor  SET Anchor = ? WHERE CID = ?"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    if (!$stmt->bind_param('ss', $_SESSION["next"], $cid)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        if ($stmt->errno == 1062) {
            die(header('location: ../error.php?msg=te'));
        }
    }

    $stmt->close();
    $_SESSION['next'] = $_SESSION['next'] + 1;
}


if ($_SESSION['next'] < count($_SESSION['version'])) {
    $mysqli->close();
    header("Location: ../task.php");
    exit();
} else {
    //    Fetch submission code from the database
    if (!($stmt = $mysqli->prepare("SELECT v_hash FROM validation_code WHERE v_id=?"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    if (!$stmt->bind_param('s', $_SESSION["scid"])) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    $stmt->bind_result($scid);
    $stmt->fetch();

    $stmt->close();
    $mysqli->close();

    header("Location: ../submit.php?scid=" . $scid);

    exit();
}