<?php
include_once 'globals.php';
include 'utils.php';

$myheaders = "Content-Security-Policy: default-src 'none';
Content-Security-Policy: style-src: 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css';
Content-Security-Policy: script-src: 'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js';
Content-Security-Policy: image-src: 'all';";
issue_headers(explode("\n", $myheaders));

if(isset($_GET['source'])) {
    highlight_file(__FILE__);
    die();
}
if (isset($_POST['url']) && is_string($_POST['url'])) {
    $url = $_POST['url'];
    if(validate_url($url)){
        $ch = curl_init($url);
        $headers = &set_curl_options($ch);
        $data = curl_exec($ch);
        if(isset($headers['content-type']) && 
        preg_match("/^image\/(\w+)/", $headers['content-type'][0], $matches)){
            $extension = $matches[1];
            trigger_img_download("image", $extension, $data);
        }
        else { $error = "Content is not an image"; }
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phantom</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <style>
        body {
            background: linear-gradient(to right, rgba(0, 4, 40,.4), rgba(0, 78, 146,.6)), url('https://wallpapers.com/images/featured/ghost-wj0blqfz7qcbaa7r.jpg');
            background-repeat: no-repeat;
            background-size: 100vw 100vh;
            background-attachment: fixed;
            background-position: top left;
        }
    </style>
</head>

<body class="white-text">
    <header>
    </header>
    <main>
        <div class="container">
            <h2 class="row">Welcome 👻</h2>
            <p class="row">
                Welcome to the phantom gateway. <br>
                You can easily download images by providing the image url below. <br>
            </p>
            <div class="row">
                <div class="col l6">
                    <div class="row">
                        <form method="post">
                            <div class="input-field">
                                <input type="text" name="url" placeholder="URL" style="color: white;">
                                <label for="url">Enter your url</label>
                            </div>
                            <button type="submit" class="btn waves-effect waves-button-input">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
            <p class="row"><?= isset($error) ? "<b>ERROR:</b> ".htmlspecialchars($error) : "" ?></p>
        </div>
    </main>
    <footer>

    </footer>
    <!-- Compiled and minified JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>

</body>

</html>