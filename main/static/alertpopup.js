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

var Engine;
var Render;
var World;
var Bodies;
var engine;

function loadAlerts() {
 // $("#logs").append("Fetching Alerts: " + new Date($.now())+"</br>" );
  $.getJSON('/alerts_api', null, handleAlerts ).fail(
    function(jqxhr, textStatus, error) {
      setTimeout(loadAlerts, 1000);
    });
}

function handleAlerts(resp) {
  var alerts = resp.alerts;
  for (var i = 0; i <= alerts.length-1; i++) {
    var data = alerts[i];

    //$("#logs").append("Have not seen this user: " + data['id'] + "</br>");

    if( data['type'] == "SUB" ) {
      makeSub( data['id'], data['image'] );
    }
  }
}

function makeSub(id, img_url) {
    var pumpkin = Bodies.circle(200,200,24, {render: {sprite:{ texture: "/pumpkinImage?url=https://yt3.ggpht.com/-KvBjE1iQ-Yk/AAAAAAAAAAI/AAAAAAAAAAA/8y92vRZBW2s/s88-c-k-no-mo-rj-c0xffffff/photo.jpg"}}});

    World.add(engine.world,[pumpkin]);


}

$(document).ready( function() {

    setInterval( loadAlerts, 1000 );

    //module aliases
     Engine = Matter.Engine;
     Render = Matter.Render;
     World = Matter.World;
     Bodies = Matter.Bodies;

     // create an engine
     engine = Engine.create();

     // create a renderer
     var render = Render.create({ element: document.body, engine: engine, options : {width: 1280, height:720, wireframes:false} });

     // create two boxes and a ground
     var ground = Bodies.rectangle(0, 720, 12080, 5, { isStatic: true });
     var leftWall = Bodies.rectangle(0, 0, 5, 10000, { isStatic: true });
     var rightWall = Bodies.rectangle(1280, 0, 5, 10000, { isStatic: true });

     // add all of the bodies to the world
     World.add(engine.world, [ground, leftWall, rightWall]);

     // run the engine
     Engine.run(engine);

     // run the renderer
     Render.run(render);


} );
