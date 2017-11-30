function loadDashboard(page, dashboard) {
	var url = "/dashboards/page/"+dashboard+"/"+page+"/";
	console.log("Getting", url);
	axios.get(url).then(function (response) {
		$('#content').html(response.data);
	}).catch(function (error) {
		console.log(error);
	});
	$(".sparkline-embeded").each(function () {
	  var $this = $(this);
	  $this.sparkline('html', $this.data());
	});
}

$(document).ready(function () {
	loadDashboard("index", "{{ dashboard }}");
	$(".sparkline").each(function () {
	  var $this = $(this);
	  $this.sparkline('html', $this.data());
	});
});