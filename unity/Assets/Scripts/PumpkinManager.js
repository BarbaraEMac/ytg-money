#pragma strict

var nameText : UnityEngine.UI.Text;
var backgroundRenderer : SpriteRenderer;
var profileRenderer : SpriteRenderer;

private var pumpkinOrange : Color = Color(1.0, 0.4, 0.0);

function Start () {
    if (backgroundRenderer.color == Color.white) {
	SetColor(pumpkinOrange);
    }
}

function Update () {
    
}

function OnMouseDown() {
    Debug.Log("Pumpkin Clicked!");
    StartCoroutine(AnimatedScale(2.0f, 0.5f));
    SetColor(Color.red);
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

function SetColor(newColor : Color){
    backgroundRenderer.color = newColor;
}

function SetName(newName : String){
    nameText.text = newName;
}

function SetProfile(newSprite : Sprite){
    profileRenderer.sprite = newSprite;
}