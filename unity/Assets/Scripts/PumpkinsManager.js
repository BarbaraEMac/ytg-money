#pragma strict

var pumpkinPrefab : GameObject;
var pumpkinsToAdd : int = 0;
var secondsBetweenAdditions : float = 0.5f;

private var superBlue : Color = Color(21.0/255.0, 101.0/255.0, 192.0/255.0);
private var superTeal : Color = Color(0.0, 229.0/255.0, 1);
private var superGreen : Color = Color(29.0/255.0, 233.0/255.0, 182.0/255.0);
private var superYellow : Color = Color(1, 202.0/255.0, 40.0/255.0);
private var superOrange : Color = Color(245.0/255.0, 124.0/255.0, 0);
private var superPink : Color = Color(233.0/255.0, 30.0/255.0, 99.0/255.0);
private var superRed : Color = Color(230.0/255.0, 33.0/255.0, 23.0/255.0);

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
    var pumpkinColor : Color = ColorForAmmount(newPumpkin.amount);
    newPumpkinObject.SendMessage("SetColor", pumpkinColor);
}

class Pumpkin {
    var name : String;
    var profile : Sprite;
    var amount : int;
}

function ColorForAmmount(dollarAmmount : int) {
    if (dollarAmmount < 2) {
        return superBlue;
    } else if (dollarAmmount < 5) {
        return superTeal;
    } else if (dollarAmmount < 10) {
        return superGreen;
    } else if (dollarAmmount < 20) {
        return superYellow;
    } else if (dollarAmmount < 50) {
        return superOrange;
    } else if (dollarAmmount < 100) {
        return superPink;
    }
    return superRed;
}