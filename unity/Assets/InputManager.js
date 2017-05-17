#pragma strict

function Start () {
    Debug.Log("Hello World");
}

function Update () {
    var inputStr : String = Input.inputString;
    var numberPKeyPresses : int = numStringOccurances(inputStr, "p");
    if (numberPKeyPresses > 0) {
	gameObject.SendMessage("addPumpkin");
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