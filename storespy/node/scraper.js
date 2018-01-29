'use strict';

var appId = process.argv[2]
var gplay = require('google-play-scraper');
 
gplay.app({appId: appId})
    .then(console.log, console.log);