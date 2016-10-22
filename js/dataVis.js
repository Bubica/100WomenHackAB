	//get data and set as variable
	//pass data to functions
	init();

function init () {
	pieChart();
	ageMatch();
	geoMatch();
	$()
}		

function pieChart (){
	console.log('chart called');
	var config = {
		type: 'pie',
		data: {
			datasets: [{
				data: [
				120,
				180
				],
				backgroundColor: [
				"#F7464A",
				"#46BFBD",
				]
			}],
			labels: [
			"Female",
			"Male",
			]
		},
		options: {
			responsive: true
		}
	};

	window.onload = function() {
		var ctx = document.getElementById("chart-area").getContext("2d");
		window.myPie = new Chart(ctx, config);
	};
}

function ageMatch () {
	console.log('called');
	var user = "dummydata";
	user_name = document.createElement('h3');
	user_name.innerHTML = user;
	container = document.getElementById('user_age_container');
	container.appendChild(user_name);    

}

function geoMatch () {

}