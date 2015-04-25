function sendToServer(){
	var date = new Date();
	console.log(date);
  var http = new XMLHttpRequest();
	var url = "http://student-monitor.appspot.com/chrome";
	//var params = "datas=clicked&ts="+Date.now();
	var params = "email=ASHOK"+"&eventType="+"Mouse"+"&urlLink="+"mail.google.com"+"&datas="+"moved"+"&timeStamp="+date;
	//alert(params);
	http.open("POST", url, true);

	//Send the proper header information along with the request
	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	http.setRequestHeader("Access-Control-Allow-Origin", "*");
	//http.setRequestHeader("Content-length", params.length);
	http.setRequestHeader("Connection", "close");

	http.onreadystatechange = function() {//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			//alert(http.responseText);
			console.log("Send Data to server: "+http.status+"| "+http.responseText);
		}
	}
	http.send(params);
}
sendToServer();