#pragma strict

var pumpkinPrefab : GameObject;
var pumpkinsToAdd : int = 0;
var secondsBetweenAdditions : float = 0.5f;

function Start () {
    
}

function Update () {
	
}

function enqueuePumpkin(newPumpkin : Pumpkin) {
    pumpkinsToAdd ++;
    yield WaitForSeconds(secondsBetweenAdditions * pumpkinsToAdd);
    pumpkinsToAdd --;
    instantiatePumpkinPrefab(newPumpkin);
}

function instantiatePumpkinPrefab(newPumpkin : Pumpkin) {
    var newPumpkinObject : GameObject = Instantiate(pumpkinPrefab);

    newPumpkinObject.transform.position.y = 6;
    newPumpkinObject.transform.position.x = Random.Range(-1.0f, 1.0f);
    newPumpkinObject.transform.eulerAngles.z = Random.Range(-40.0f, 40.0f);

    newPumpkinObject.SendMessage("SetName", newPumpkin.name);
    if (newPumpkin.profile != null) {
        newPumpkinObject.SendMessage("SetProfile", newPumpkin.profile);
    }
}

class Pumpkin {
    var name : String;
    var profile : Sprite;
}