function loadDashboard(name) {
	var url = "/dashboards/page/"+name+"/";
	console.log("Getting", url);
	axios.get(url).then(function (response) {
		$('#content').html(response.data);
	}).catch(function (error) {
		console.log(error);
	});
}

$(document).ready(function () {
	loadDashboard("{{ slug }}");
});