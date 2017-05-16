#pragma strict

var pumpkinOrange : Color = Color(1.0, 0.4, 0.0);
var topLayerDepth : float = 0.0f;

function Start () {
    ChangeColor(pumpkinOrange);
    // topLayerDepth -= 1;
    // gameObject.transform.position.z = topLayerDepth;
}

function Update () {
    
}

function OnMouseDown() {
    Debug.Log("Pumpkin Clicked!");
    StartCoroutine(AnimatedScale(2.0f, 0.5f));
    ChangeColor(Color.red);
}

function AnimatedScale(factor : float, duration : float) {
    Debug.Log("Animation started");
    var framesPerSecond : float = 60.0f;
    var incriment : float = (factor - 1) / (framesPerSecond * duration);
    var initialScale : Vector3 = gameObject.transform.localScale;
    for (var i : float = 0; i < duration * framesPerSecond; i++) { 
	Debug.Log(i);
	gameObject.transform.localScale = initialScale * (1 + i*incriment);
	yield;
    }
}

function ChangeColor(newColor : Color){
    Debug.Log("Changing Color!");
    var background : GameObject = gameObject.transform.Find("background").gameObject;
    var backgroundRenderer : SpriteRenderer;
    backgroundRenderer = background.GetComponent(SpriteRenderer) as SpriteRenderer;
    backgroundRenderer.color = newColor;
}