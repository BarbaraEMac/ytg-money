#pragma strict

var nameText : UnityEngine.UI.Text;
var backgroundRenderer : SpriteRenderer;
var highlightRenderer : SpriteRenderer;
var profileRenderer : SpriteRenderer;

private var pumpkinOrange : Color = Color(1.0, 0.4, 0.0);
private var isMoving = false;
private var pumpkinBody : Rigidbody2D;

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