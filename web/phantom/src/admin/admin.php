<?php
function issue_headers(array $headers) {
    foreach($headers as $header) {
        header($header);
    }
}
function execute_cmd(string $cmd): string{
    // TODO
    return "Not yet implemented";
}

$headers = "Content-Security-Policy: default-src 'none'; frame-ancestors 'none';";
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $output = execute_cmd($cmd);
    $headers .= "\nX-Command-Executed: $cmd";
}
issue_headers(explode("\n", $headers));
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin panel</title>
</head>

<body>
    <header></header>
    <main>
        <div>
            <p>Some very very secret stuff:</p>
            <ul>
                <li><b>Admin password</b>: Unknown</li>
                <li><b>Some other stuff</b>: Whatever</li>
                <li><b>Flag</b>: <?= isset($_ENV['FLAG']) ? $_ENV['FLAG'] : "REDACTED" ?></li>
            </ul>
        </div>
    </main>
    <footer></footer>
</body>

</html>