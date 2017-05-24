#pragma strict

var pumpkinPrefab : GameObject;
var pumpkinsToAdd : int = 0;
var secondsBetweenAdditions : float = .5f;

private var superLightBlue : Color = Color(21.0/255.0, 101.0/255.0, 192.0/255.0);
private var superLightTeal : Color = Color(0.0, 229.0/255.0, 1);
private var superLightGreen : Color = Color(29.0/255.0, 233.0/255.0, 182.0/255.0);
private var superLightYellow : Color = Color(1, 202.0/255.0, 40.0/255.0);
private var superLightOrange : Color = Color(245.0/255.0, 124.0/255.0, 0);
private var superLightPink : Color = Color(233.0/255.0, 30.0/255.0, 99.0/255.0);
private var superLightRed : Color = Color(230.0/255.0, 33.0/255.0, 23.0/255.0);

private var superDarkBlue : Color = Color(15.0/255.0, 72.0/255.0, 137.0/255.0);
private var superDarkTeal : Color = Color(0.0, 184.0/255.0, 212.0/255.0);
private var superDarkGreen : Color = Color(0.0, 191.0/255.0, 165.0/255.0);
private var superDarkYellow : Color = Color(255.0, 179.0/255.0, 0.0);
private var superDarkOrange : Color = Color(230.0/255.0, 81.0/255.0, 0.0);
private var superDarkPink : Color = Color(194.0/255.0, 24.0/255.0, 91.0/255.0);
private var superDarkRed : Color = Color(208.0/255.0, 0.0, 0.0);

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
    var pumpkinColor : Color = PrimaryColorForAmount(newPumpkin.amount);
    newPumpkinObject.SendMessage("SetPrimaryColor", pumpkinColor);
    var pumpkinHighlightColor : Color = HighlightColorForAmount(newPumpkin.amount);
    newPumpkinObject.SendMessage("SetHighlightColor", pumpkinHighlightColor);
}

class Pumpkin {
    var name : String;
    var profile : Sprite;
    var amount : int;
}

function PrimaryColorForAmount(dollarAmmount : int) {
    if (dollarAmmount < 2) {
        return superLightBlue;
    } else if (dollarAmmount < 5) {
        return superLightTeal;
    } else if (dollarAmmount < 10) {
        return superLightGreen;
    } else if (dollarAmmount < 20) {
        return superLightYellow;
    } else if (dollarAmmount < 50) {
        return superLightOrange;
    } else if (dollarAmmount < 100) {
        return superLightPink;
    }
    return superLightRed;
}

function HighlightColorForAmount(dollarAmmount : int) {
    if (dollarAmmount < 2) {
        return superDarkBlue;
    } else if (dollarAmmount < 5) {
        return superDarkTeal;
    } else if (dollarAmmount < 10) {
        return superDarkGreen;
    } else if (dollarAmmount < 20) {
        return superDarkYellow;
    } else if (dollarAmmount < 50) {
        return superDarkOrange;
    } else if (dollarAmmount < 100) {
        return superDarkPink;
    }
    return superDarkRed;
}