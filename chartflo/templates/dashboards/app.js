function loadDashboard(page, dashboard) {
	var url = "/dashboards/page/"+dashboard+"/"+page+"/";
	console.log("Getting", url);
	axios.get(url).then(function (response) {
		$('#content').html(response.data);
	}).catch(function (error) {
		console.log(error);
	});
}

$(document).ready(function () {
	loadDashboard("index", "{{ dashboard }}");
});