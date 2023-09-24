#! /bin/bash
read url;
node admin.js "$url" |& tee -a log.txt
