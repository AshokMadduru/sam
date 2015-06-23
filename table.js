var start= new Date(2015,3,27);
 alert(start);
// var next = new Date(start);
// next.setDate(start.getDate() + 1);
// alert(next.toLocaleDateString());
table();
function table(){
	var next= new Date(start);
	var tab = document.getElementById("table");

	var header = tab.createTHead();
	var row = header.insertRow(0);
	for(i=0;i<7;i++){
		var cell = row.insertCell(0);
		if(i==0){
			cell.innerHTML = "<input onclick = forward() type = \"image\" src=\"/images/gt.jpg\" width=25px height=25px>"
		}else{
			cell.innerHTML = " ";
		}
	}
	var row = header.insertRow(1);
	for(i=0;i<7;i++){
		var cell = row.insertCell(-1);
		cell.innerHTML = next.toLocaleDateString() 
		next.setDate(next.getDate() + 1);
		start = new Date(next);
	}
}
function forward(){
	var next= new Date(start);
	var tab = document.getElementById("table");
	tab.deleteTHead();

	var header = tab.createTHead();
	var row = header.insertRow(0);
	if(start.toLocaleDateString().toString() == "01/06/2015"){
		for(i=0;i<7;i++){
			var cell = row.insertCell(0);
			if(i==6){
			cell.innerHTML = "<input onclick = backward() type = \"image\" src=\"/images/lt.jpg\" width=25px height=25px>"
			}else{
				cell.innerHTML = " ";
			}
		}
	}else{
		for(i=0;i<7;i++){
			var cell = row.insertCell(0);
			if(i==0){
				cell.innerHTML = "<input onclick = forward() type = \"image\" src=\"gt.jpg\" width=25px height=25px>"
			}else if(i==6){
				cell.innerHTML = "<input onclick = backward() type = \"image\" src=\"lt.jpg\" width=25px height=25px>"
			}else{
				cell.innerHTML = " ";
			}
		}
	}
	

	var row = header.insertRow(1);
	for(i=0;i<7;i++){
		var cell = row.insertCell(-1);
		cell.innerHTML = next.toLocaleDateString() 
		next.setDate(next.getDate() + 1);
		start = new Date(next);
	}

}

function backward(){
	var next= new Date(start);
	next.setDate(next.getDate()-14);
	var tab = document.getElementById("table");
	tab.deleteTHead();

	var header = tab.createTHead();
	var row = header.insertRow(0);

	if(next.toLocaleDateString().toString() == "27/04/2015"){
		for(i=0;i<7;i++){
			var cell = row.insertCell(0);
			if(i==0){
				cell.innerHTML = "<input onclick = forward() type = \"image\" src=\"gt.jpg\" width=25px height=25px>"
			}else{
				cell.innerHTML = " ";
			}
		}
	}else{
		for(i=0;i<7;i++){
			var cell = row.insertCell(0);
			if(i==0){
				cell.innerHTML = "<input onclick = forward() type = \"image\" src=\"gt.jpg\" width=25px height=25px>"
			}else if(i==6){
				cell.innerHTML = "<input onclick = backward() type = \"image\" src=\"lt.jpg\" width=25px height=25px>"
			}else{
				cell.innerHTML = " ";
			}
		}
	}
	var row = header.insertRow(1);
	for(i=0;i<7;i++){
		var cell = row.insertCell(-1);
		cell.innerHTML = next.toLocaleDateString() 
		next.setDate(next.getDate() + 1);
		start = new Date(next);
	}
}