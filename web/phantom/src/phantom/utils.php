<?php
include_once 'globals.php';

function issue_headers(array $headers) {
    foreach($headers as $header) {
        header($header);
    }
}

function trigger_img_download(string $filename, string $extension, string $data): void
{
    header("Content-Description: File Transfer");
    header("Content-Type: application/$extension");
    header("Content-Disposition: attachment; filename=$filename.$extension");
    header('Content-Transfer-Encoding: binary');
    header('Cache-Control: must-revalidate, posst-check=0, pre-check=0');
    echo $data;
    die();
}

function valid_scheme(string $scheme): bool
{
    return in_array($scheme, ["http", "https"]);
}

function valid_host(string $host): bool
{
    return !in_array($host, ["localhost", "127.0.0.1", "0.0.0.0"]);
}

function validate_url(string $url): bool
{
    global $error;
    $valid = false;
    if (filter_var($url, FILTER_VALIDATE_URL)) {
        $parsed = parse_url($url);
        $valid = valid_scheme($parsed['scheme']) && valid_host($parsed['host']);
    }
    if (!$valid) {
        $error = "Invalid URL";
    }
    return $valid;
}

// Returns an array of headers which will be initialized on curl_exec
function &set_curl_options(&$ch){
    $headers = [];
    /* SET CURL OPTIONS:
       1. User agent must be set to real browsers because some websites do not allow curl requests (CURLOPT_USERAGENT)
       2. Headers need to be parsed to retrieve the content-type later (CURLOPT_HEADERFUNCTION)
       3. Avoid DOS by aborting when response body is too big (CURLOPT_PROGRESSFUNCTION) 
    */
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36");
    curl_setopt(
        $ch,
        CURLOPT_HEADERFUNCTION,
        function ($curl, $header) use (&$headers) {
            $len = strlen($header);
            $header = explode(':', $header, 2);
            if (count($header) == 2) { // ignore invalid headers
                $headers[strtolower(trim($header[0]))][] = trim($header[1]);
            }
            return $len;
        }
    );
    curl_setopt($ch, CURLOPT_BUFFERSIZE, 1024);
    curl_setopt($ch, CURLOPT_NOPROGRESS, false);
    curl_setopt(
        $ch,
        CURLOPT_PROGRESSFUNCTION,
        function ($curl, $expected_download, $downloaded, $expected_upload, $uploaded) use (&$error) {
            if ($downloaded > (16 * 1024 * 1024)) {
                $error = "Content is too big";
                return 1;
            }
            return 0;
        }
    );
    return $headers;
}