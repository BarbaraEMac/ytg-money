#pragma strict

function Start () {
    var url = "http://www.ytg-money.appspot.com/alerts_api";
    var www : WWW = new WWW(url);

    yield www;

    if (www.error == null) {
	Debug.Log("success!");
	printResponseHeaders(www);
// 	var alerts : AlertArray;
// 	alerts = JsonUtility.FromJson.<AlertArray>(www.text);
	var alerts : Alert[];
	alerts = JsonUtility.FromJson.<Alert[]>(www.text);
	// Debug.Log(alerts[0].name);
    } else {
	Debug.Log("error: " + www.error);
    }
}

function Update () {
	
}

function printResponseHeaders(www : WWW) {
    if (www.responseHeaders.Count > 0) {
        for (var entry in www.responseHeaders) {
            Debug.Log(entry.Key + ": " + entry.Value);
        }
    }
}

public class Alert {
    public var name : String;
}

public class AlertArray {
    public var alerts : Alert[];
}
