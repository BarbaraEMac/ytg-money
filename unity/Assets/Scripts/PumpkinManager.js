#pragma strict

var nameText : UnityEngine.UI.Text;
var backgroundRenderer : SpriteRenderer;
var highlightRenderer : SpriteRenderer;
var profileRenderer : SpriteRenderer;

private var pumpkinOrange : Color = Color(1.0, 0.4, 0.0);
private var isMoving = false;
private var pumpkinBody : Rigidbody2D;
private var pumpkin : Pumpkin;

private var superLightBlue : Color = Color(21.0/255.0, 101.0/255.0,
                                           192.0/255.0);
private var superLightTeal : Color = Color(0.0, 229.0/255.0, 1);
private var superLightGreen : Color = Color(29.0/255.0, 233.0/255.0,
                                            182.0/255.0);
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
    if (backgroundRenderer.color == Color.white) {
	SetPrimaryColor(pumpkinOrange);
    }
    
    pumpkinBody = gameObject.GetComponentInChildren(Rigidbody2D);
    if (pumpkinBody == null) {
        Debug.LogError("PumpkinManager GameObject requires Rigidbody2D.");
    }
}

function Update () {
    if (pumpkinBody.velocity.magnitude < 0.001 &&
        pumpkinBody.angularVelocity < 0.001) {
        if (isMoving) {
            isMoving = false;
            OnStopMoving();
        }
    } else {
        if (!isMoving) {
            isMoving = true;
            OnStartMoving();
        }
    }
}

function OnStopMoving() {
    Debug.Log("Pumpkin stopped");
}

function OnStartMoving() {
    Debug.Log("Pumpkin started moving");
}

function OnMouseDown() {
    Debug.Log("Pumpkin Clicked!");
    StartCoroutine(AnimatedScale(2.0f, 0.5f));
    SetPrimaryColor(Color.red);
}

function AnimatedScale(factor : float, duration : float) {
    var framesPerSecond : float = 60.0f;
    var incriment : float = (factor - 1) / (framesPerSecond * duration);
    var initialScale : Vector3 = gameObject.transform.localScale;
    for (var i : float = 0; i < duration * framesPerSecond; i++) { 
	Debug.Log(i);
	gameObject.transform.localScale = initialScale * (1 + i*incriment);
	yield;
    }
}

function SetPrimaryColor(newColor : Color){
    backgroundRenderer.color = newColor;
}

function SetHighlightColor(newColor : Color){
    highlightRenderer.color = newColor;
}

function SetName(newName : String){
    // nameText.text = newName;
}

function SetProfile(newSprite : Sprite){
    profileRenderer.sprite = newSprite;
}

function SetPumpkin (newPumpkin : Pumpkin) {
    pumpkin = newPumpkin;
    if (pumpkin.profile != null) {
        SetProfile(pumpkin.profile);
    }
    SetPrimaryColor(PrimaryColorForAmount(pumpkin.amount));
    SetHighlightColor(HighlightColorForAmount(pumpkin.amount));
    gameObject.transform.position.x = pumpkin.xPosition;
    gameObject.transform.position.y = pumpkin.yPosition;
    gameObject.transform.eulerAngles.z = pumpkin.rotation;
}

class Pumpkin {
    var name : String;
    var profile : Sprite;
    var amount : int;
    var xPosition : float;
    var yPosition : float;
    var rotation : float;
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