#pragma strict

var pumpkinObject : GameObject;

function Start () {
    
}

function Update () {
	
}

function addPumpkin() {
    var newPumpkin : GameObject = Instantiate(pumpkinObject);
    newPumpkin.transform.position.y = 6;
    newPumpkin.transform.position.x = Random.Range(-1.0f, 1.0f);
    newPumpkin.transform.eulerAngles.z = Random.Range(-40.0f, 40.0f);
    newPumpkin.SendMessage("SetName", "BarbaraMacdonald");
}