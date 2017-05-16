#pragma strict

var pumpkinObject : GameObject;

function Start () {
    Debug.Log("Hello World");
}

function Update () {
    var inputStr : String = Input.inputString;
    var numberPKeyPresses : int = numStringOccurances(inputStr, "p");
    if (numberPKeyPresses > 0) {
	addPumpkin();
    }
}

function numStringOccurances (source : String, target : String) {
    var i = 0;
    var count = 0;
    while (true) {
        i = source.IndexOf(target, i);
        if (i < 0) {
            break;
        }
        count ++;
        i++;
    }
    return count;
}

function addPumpkin() {
    var newPumpkin : GameObject = Instantiate(pumpkinObject);
    newPumpkin.transform.position.y = 6;
    newPumpkin.transform.position.x = Random.Range(-1.0f, 1.0f);
    newPumpkin.transform.eulerAngles.z = Random.Range(-40.0f, 40.0f);
}