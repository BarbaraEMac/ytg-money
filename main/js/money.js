var DEFAULT_ALERT_TIME = 5000;
var seenAlert = {};
var sponsorSize = 150;
var users = [];
var theGrid = [];
var sponsors = [];
var maxHeight = 720;
var maxWidth = 1280;
var currX = 0;
var currY = 0;

function loadAlerts() {
 // $("#logs").append("Fetching Alerts: " + new Date($.now())+"</br>" );
  $.getJSON('/moneyAlerts', null, handleAlerts ).fail(
    function(jqxhr, textStatus, error) {
      setTimeout(loadAlerts, 1000);
    });
}

function handleAlerts(resp) {
  var alerts = resp.alerts;
  for (var i = 0; i <= alerts.length-1; i++) {
    var data = alerts[i];

    if(!seenAlert[data['id']]) {
        seenAlert[data['id']] = true;

        if( data['type'] == "SUPER" ){

            makeSuper( data['channel_id'], data['image'], data['name'], data['amount'] );

        } else if( data['type'] == "SPONSOR" ) {

            makeSponsor( data['channel_id'], data['image'], data['name'] );
        }
    }
  }
}

function makeSuper( channel_id, img_url, name, amount ) {
    // Find a battleship spot for it
    var size = priceToSize( amount );
    var loc = findXY_opt( size );
    markTaken(loc['x'], loc['y'], size);


    // Make the div and image
    var foo = $('<div id="' + channel_id + '" class="th"></div>');
    var bar = $('<img src="'+ img_url + '" />');

    var avatarSize = Math.round( size * 0.4 );
    var avatarLoc = Math.round( (size-avatarSize-8) / 2 );

    // Style them up
    foo.css("position", "absolute");
    foo.css("height", size+"px");
    foo.css("width", size+"px");
    foo.css("left", loc['x']+"px");
    foo.css("top", loc['y']+"px");
    foo.css("backgroundImage", "url('/static/heart.png')");
    foo.css("backgroundSize", size+"px "+size + "px");

    bar.css("position", "absolute");
    bar.css("height", avatarSize+"px");
    bar.css("width", avatarSize+"px");
    bar.css("top", avatarLoc+"px");
    bar.css("left", avatarLoc+"px");
    bar.css("border-radius", "50%");
    bar.css("border-style", "solid");
    bar.css("border-color", "#00ff00");
    bar.css("border-width", "5px");

    // Put them in the page
    foo.append ( bar );
    $("#container").append( foo );
}

function makeSponsor( channel_id, img_url, name ) {
    if( sponsors[channel_id] == true ) {
        return;
    }
    sponsors[channel_id] = true;

    // Find a battleship spot for it
    var loc = findXY_opt( sponsorSize );
    markTaken(loc['x'], loc['y'], sponsorSize);

    // Make the div and image
    var foo = $('<div id="' + channel_id + '" class="th"></div>');
    var bar = $('<img src="'+ img_url + '" />');

    var avatarSize = Math.round( sponsorSize * 0.4 );
    var avatarLoc = Math.round( (sponsorSize-avatarSize-8) / 2 );

    // Style them up
    foo.css("position", "absolute");
    foo.css("height", sponsorSize+"px");
    foo.css("width", sponsorSize+"px");
    foo.css("left", loc['x']+"px");
    foo.css("top", loc['y']+"px");
    foo.css("backgroundImage", "url('/static/heart_vines.png')");
    foo.css("backgroundSize", sponsorSize+"px "+sponsorSize + "px");

    bar.css("position", "absolute");
    bar.css("height", avatarSize+"px");
    bar.css("width", avatarSize+"px");
    bar.css("top", avatarLoc+"px");
    bar.css("left", avatarLoc+"px");
    bar.css("border-radius", "50%");
    bar.css("border-style", "solid");
    bar.css("border-color", "#00ff00");
    bar.css("border-width", "5px");

    // Put them in the page
    foo.append ( bar );
    $("#container").append( foo );
}

function markTaken(x, y, size) {

    for( var i = x; i < x+size; i++ ){
        for( var j = y; j < y+size; j ++ ){
            theGrid[i][j] = true;
        }
    }
}

function initialize() {

    for(var i = 0; i < maxWidth; i++) {
        theGrid[i] = [];

        for(var j = 0; j < maxHeight; j++) {
            theGrid[i][j] = false;
        }
    }
}

function priceToSize( amount ) {
    var size = 0;

    if( amount < 2 ) {
        size = 75;
    } else if ( amount < 5 ) {
        size = 110;
    } else if ( amount < 10 ) {
        size = 150;
    } else if ( amount < 25 ) {
        size = 175;
    } else if ( amount < 50 ) {
        size = 250;
    } else if ( amount < 100 ) {
        size = 300;
    } else {
        size = 350;
    }

    return size;
}

function findXY_opt( size ){
    $("#logs").html("Opt");
    for( var i = 0; i < maxWidth; i ++) {

        for( var j = 0; j < maxHeight; j++ ){

            if( tryXY(i, j, size) ) {
                return {x: i, y: j};
            }
        }
    }

    return findXY(size);
}

function findXY( size ) {
    $("#logs").html("Random");
    var locX = Math.round( Math.random()*(maxWidth-size) );
    var locY = Math.round( Math.random()*(maxHeight-size) );
    var overlap = Math.round( size*0.15 );
    var count = 1000;
    if( size < 120 ) count *= 100;

    while( !tryXY(locX, locY, size) ) {
        locX = Math.round( Math.random()*(maxWidth-size) );
        locY = Math.round( Math.random()*(maxHeight-size) );

        count -= 1;
        if( count == 0 ){
            return {x:locX, y:locY};
        }
    }
    return {x:locX, y:locY};
}

function tryXY(x, y, size){
    $("#logs").html("Trying " + x + " " + y + " " + size );

    for( var i = x; i <= x+size; i++ ){

        for( var j = y; j <= y+size; j ++ ){
            if( theGrid[i][j] == true ) {
                return false;
            }
        }
    }
    return true;
}

$(document).ready( function() {

    initialize();

    $('body').keyup(function(e){
        if(e.keyCode == 32){
            makeSponsor(Math.random(), "https://yt3.ggpht.com/-KvBjE1iQ-Yk/AAAAAAAAAAI/AAAAAAAAAAA/8y92vRZBW2s/s88-c-k-no-mo-rj-c0xffffff/photo.jpg", "name");
        } else if( e.keyCode == 65 ) {
            var a = Math.random()*500;
            makeSponsor(Math.random(), "https://yt3.ggpht.com/-KvBjE1iQ-Yk/AAAAAAAAAAI/AAAAAAAAAAA/8y92vRZBW2s/s88-c-k-no-mo-rj-c0xffffff/photo.jpg", "name", a);
        } else {
            var a = 0;
        }
    });

    setInterval( loadAlerts, 1000 );
} );
