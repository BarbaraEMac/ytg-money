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

function loadAlerts() {
  $("#logs").append("Fetching Alerts: " + new Date($.now())+"</br>" );
  $.getJSON('/alerts_api', null, handleAlerts ).fail(
    function(jqxhr, textStatus, error) {
      setTimeout(loadAlerts, 1000);
    });
}

function handleAlerts(resp) {
  var alerts = resp.alerts;
  var subs = [];

  for (var i = 0; i <= alerts.length-1; i++) {
      var data = alerts[i];

      $("#logs").append("Have not seen this user: " + data['id'] + "</br>");

      if( data['type'] == "SUB" ) {
        makeSub( data['id'], data['image'] );
      }

  }
}

function makeSub(id, img_url) {
  var foo = $('<div id="' + id + '" class="th"> </div>');

  foo.css("position", "absolute");
  foo.css("height", "150px");
  foo.css("top", "0px");
  foo.css("left", (Math.round( Math.random()*1280))+"px");
  foo.css("backgroundImage", "url('/static/BarbBot_25.png')");
  foo.css("backgroundSize", "150px 150px");

  var bar = $('<img src="'+ img_url + '" />');
  bar.css("position", "absolute");
  bar.css("height", "95px");
  bar.css("width", "125px");
  bar.css("top", "40px");
  bar.css("left", "12px");
  bar.css("border-radius", "50%");
  bar.appendTo(foo);

  foo.appendTo("#world");

  foo.throwable({shape:"circle",autostart:true,bounce:0.1,gravity:{x:0,y:0.1}});
}

$(document).ready( function() {
    for(var i = 0; i <= 20; i++ ) {
    setTimeout( function() { loadAlerts(); }, 1000 );
    }
} );
