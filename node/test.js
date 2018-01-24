var gplay = require('google-play-scraper');
 
gplay.app({appId: 'com.android.chrome'})
    .then(console.log, console.log);