function loadDashboard(page, dashboard) {
	var url = "/dashboards/page/"+dashboard+"/"+page+"/";
	console.log("Getting", url);
	var spinner = '<div class="text-center" style="width:100%;margin-top:5em;opacity:0.6">';
	spinner = spinner + '<i class="fa fa-spinner fa-spin fa-5x fa-fw"></i>\n</div>';
	$("#content").html(spinner);
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