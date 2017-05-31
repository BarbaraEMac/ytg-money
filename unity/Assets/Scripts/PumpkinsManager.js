#pragma strict

var pumpkinPrefab : GameObject;
var pumpkinsToAdd : int = 0;
var secondsBetweenAdditions : float = .5f;

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

    newPumpkin.yPosition = 6;
    newPumpkin.xPosition = Random.Range(-1.0f, 1.0f);
    newPumpkin.rotation = Random.Range(-40.0f, 40.0f);

    newPumpkinObject.SendMessage("SetPumpkin", newPumpkin);
}