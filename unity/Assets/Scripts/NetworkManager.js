#pragma strict

var fetchingAlerts = false;
var alertsURL = "http://www.ytg-money.appspot.com/alerts_api";

function Start () {
    // This should be moved to the update function once we have non-canned data
    fetchAlerts();
}

function Update () {

}

function fetchAlerts() {
    if (fetchingAlerts) {
        return;
    }
    fetchingAlerts = true;

    var www : WWW = new WWW(alertsURL);
    yield www;

    if (www.error == null) {
	var alerts : AlertArray;
	alerts = JsonUtility.FromJson.<AlertArray>(www.text);
	for (alert in alerts.alerts) {
            addPumpkinFromAlert(alert);
	}
    } else {
        Debug.Log("error: " + www.error);
    }

    fetchingAlerts = false;
}

function addPumpkinFromAlert(alert : Alert) {
    var pumpkin : Pumpkin = new Pumpkin();
    pumpkin.name = alert.name;

    var imageWWW : WWW = new WWW(alert.image);
    yield imageWWW;

    var h : int = imageWWW.texture.height;
    var w : int = imageWWW.texture.width;
    var imageSprite : Sprite = Sprite.Create(imageWWW.texture, 
                                             new Rect(0, 0, w, h), 
                                             new Vector2(0,0));
    pumpkin.profile = imageSprite;
    
    gameObject.SendMessage("enqueuePumpkin", pumpkin);
}

public class Alert {
    public var name : String;
    public var amount : int;
    public var sponsor : int;
    public var image : String;
    public var text : String;
    public var id : String;
}

public class AlertArray {
    public var alerts : Alert[];
}

function printResponseHeaders(www : WWW) {
    if (www.responseHeaders.Count > 0) {
        for (var entry in www.responseHeaders) {
            Debug.Log(entry.Key + ": " + entry.Value);
        }
    }
}