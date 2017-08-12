/*
  Copyright 2016 Google Inc. All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/
var DEFAULT_ALERT_TIME = 5000;
var added = false;
var count = 0;
var divIds = [];
var seenUser = {};
var pumpkinSize = 75;
var worldShown = false;

function loadAlerts() {
 // $("#logs").append("Fetching Alerts: " + new Date($.now())+"</br>" );
  $.getJSON('/subsAlerts', null, handleAlerts ).fail(
    function(jqxhr, textStatus, error) {
      setTimeout(loadAlerts, 1000);
    });
}

function handleAlerts(resp) {
  var alerts = resp.alerts;
  for (var i = 0; i <= alerts.length-1; i++) {
    var data = alerts[i];

    if(!seenUser[data['id']]) {
        seenUser[data['id']] = true;

        makeSub( data['id'], data['image']);
    }
  }
}

function makeSub(id, img_url) {
  showWorld();

  if(divIds.length == 0 ){
      return;
  }

  var bar = $('<img src="'+ img_url + '" />');
  bar.css("position", "absolute");
  bar.css("height", "47px");
  bar.css("width", "62px");
  bar.css("top", "20px");
  bar.css("left", "6px");
  bar.css("border-radius", "50%");

  var foo = $( "#"+divIds.pop() );
  foo.append( bar );
  foo.css("display", "inline");
}

function initialize() {
    for( var i = 0; i < 120; i ++ ) {
        var divName = "pump"+i;
        divIds.push( divName );

        var loc = $(window).width() - pumpkinSize - (Math.round( Math.random()*pumpkinSize));
        var foo = $('<div id="' + divName + '" class="th"></div>');

        foo.css("position", "absolute");
        foo.css("height", pumpkinSize+"px");
        foo.css("top", "0px");
        foo.css("left", loc+"px");
        foo.css("backgroundImage", "url('/static/BarbBot_25.png')");
        foo.css("backgroundSize", pumpkinSize+"px "+pumpkinSize + "px");

        $("#container").append( foo );
    }

    $(".th").throwable({containment:[0,0, $(window).width(), $(window).height()], shape:"circle",drag:true,autostart:true,damping:100,gravity:{x:0,y:2}});

    var i = divIds.length;

    for( ; i >= 0; i -- ) {
        var id = divIds.shift();
        $("#"+id).css("display", "none");
        $("#container").append( $("#"+id) );
        divIds.push(id);
    }
}

function hideWorld() {
    if( worldShown == true ) {
        worldShown = false;
        $("#container").fadeOut(2000);
    }
}
function showWorld() {
    if( worldShown == false ) {
        worldShown = true;
        $("#container").fadeIn(2000);
        setTimeout( hideWorld, 10000);
    }
}

$(document).ready( function() {

    initialize();

    $('body').keyup(function(e){
        if(e.keyCode == 32){
            // user has pressed space
            var i = divIds.length;

            for( ; i >= 0; i -- ) {
                var id = divIds.shift();
                $("#"+id).css("display", "none");
                divIds.push(id);
            }
        } else if( e.keyCode == 65 ) {
            makeSub(Math.random(), "/static/BarbBot_10.png");


        } else {
            // user has pressed space
            var i = divIds.length;

            for( ; i >= 0; i -- ) {
                var id = divIds.shift();
                $("#"+id).css("display", "inline");
                divIds.push(id);
            }
        }

    });

    setInterval( loadAlerts, 1000 );
} );
