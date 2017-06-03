#pragma strict

var fetchingAlerts = false;
private var host = "https://ytg-money.appspot.com";
private var alertsURL = host + "/alerts_api";
private var pumpkinsURL = host + "/pumpkins";
private var lastFetchTime = 0.0f;
private var fetchEverySeconds = 1.0f;

function Start () {
    fetchPumpkins();
}

function Update () {
    if (Time.time > lastFetchTime + fetchEverySeconds) {
        fetchAlerts();
        lastFetchTime += fetchEverySeconds;
    }
}

function fetchAlerts() {
    if (fetchingAlerts) {
        return;
    }
    fetchingAlerts = true;

    var www : WWW = new WWW(alertsURL);
    yield www;

    if (www.error == null) {
	var response : AlertFetchResponse;
	response = JsonUtility.FromJson.<AlertFetchResponse>(www.text);
        if (response != null) {
            for (alert in response.alerts) {
                addPumpkinFromAlert(alert);
            }
        }
    } else {
        Debug.LogError("error fetching alerts: " + www.error);
    }

    fetchingAlerts = false;
}

function fetchPumpkins(){
    var www : WWW = new WWW(pumpkinsURL);
    yield www;

    if (www.error != null) {
        Debug.LogError("error fetching pumpkins: " + www.error);
        return;
    }

    var response : PumpkinsFetchResponse;
    response = JsonUtility.FromJson.<PumpkinsFetchResponse>(www.text);
    if (response != null) {
        for (pumpkin in response.pumpkins) {
            gameObject.SendMessage("instantiatePumpkinPrefab", pumpkin);
            updateProfileAfterFetch(pumpkin.profile_URL, pumpkin);
        }
    }
}

function updateProfileAfterFetch(imageURL : String, pumpkin : Pumpkin) {
    var www : WWW = new WWW(imageURL);
    yield www;

    var sprite : Sprite = imageFromFetch(www);

    pumpkin.gameObject.SendMessage("SetProfile", sprite);
}

function imageFromFetch(imageWWW : WWW) {
    if (imageWWW.error != null) {
        Debug.LogError("error fetching pumpkin profile: " + imageWWW.error);
        return;
    }

    var h : int = imageWWW.texture.height;
    var w : int = imageWWW.texture.width;
    var imageSprite : Sprite = Sprite.Create(imageWWW.texture, 
                                             new Rect(0, 0, w, h), 
                                             new Vector2(0,0));
    return imageSprite;
}

function addPumpkinFromAlert(alert : Alert) {
    var pumpkin : Pumpkin = new Pumpkin();
    pumpkin.user_name = alert.name;
    pumpkin.amount = alert.amount;

    var imageWWW : WWW = new WWW(alert.image);
    yield imageWWW;

    pumpkin.profile = imageFromFetch(imageWWW);
    pumpkin.profile_URL = alert.image;

    pumpkin.y_position = 6;
    pumpkin.x_position = Random.Range(-1.0f, 1.0f);
    pumpkin.rotation = Random.Range(-40.0f, 40.0f);
    
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

public class AlertFetchResponse {
    public var alerts : Alert[];
}

function printResponseHeaders(www : WWW) {
    if (www.responseHeaders.Count > 0) {
        for (var entry in www.responseHeaders) {
            Debug.Log(entry.Key + ": " + entry.Value);
        }
    }
}

public class PumpkinsFetchResponse {
    public var pumpkins : Pumpkin[];
}