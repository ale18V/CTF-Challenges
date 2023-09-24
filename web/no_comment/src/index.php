<?php
$servername = getenv('DBHOST');
$username = getenv('DBUSER');
$password = getenv('DBPASS');
$dbschema = getenv("DBSCHEMA");
$db = new mysqli($servername, $username, $password, $dbschema);

if (isset($_GET['source'])) {
    highlight_file("index.php");
    die();
}

function validUsername()
{
    return isset($_POST['username'])
        && is_string($_POST['username'])
        && !stripos($_POST['username'], ' ');
}

function validPassword()
{
    return isset($_POST['password'])
        && is_string($_POST['password'])
        && !stripos($_POST['password'], ' ');
}

if (validUsername() && validPassword()) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // TODO: Add password based authentication
    $query = "SELECT name FROM USERS WHERE name=? -- and /* password='{$password}' */";
    $stmt = $db->prepare($query);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result()->fetch_assoc();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/materialize.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <title>No Comment</title>
</head>

<body class="">
    <!-- CREATE TABLE FLAG(flag varchar(255) not null primary key);  :) -->
    <div class="container">
        <h1 class="row">
            Hello <?= isset($result['name']) ? $result['name'] : 'world' ?>
        </h1>
        <p class="row">
            You can view the source code <a href="/?source">here</a>.<br>
            The page is still under production so you don't even need a password in order to login.
        </p>

        <form action="/" method="POST" class="row">
            <div class="input-field">
                <input type="text" placeholder="Username" name="username" id="username" class="validate">
            </div>
            <div class="input-field">
                <input type="text" placeholder="Password" name="password" id="password" class="validate">
            </div>

            <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                <i class="material-icons right">send</i>
            </button>
            <div></div>

        </form>
        
    </div>
    <script src="/static/js/materialize.min.js" async defer></script>
</body>

</html>
