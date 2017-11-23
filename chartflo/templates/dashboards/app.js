function loadDashboard(page, url) {
	console.log("Getting", url);
	axios.get(url).then(function (response) {
		$('#content').html(response.data);
	}).catch(function (error) {
		console.log(error);
	});
}

$(document).ready(function () {
	var url = "/dashboards/page/{{ dashboard }}/";
	loadDashboard("{{ page }}", url);
});