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

    newPumpkinObject.SendMessage("SetPumpkin", newPumpkin);
}