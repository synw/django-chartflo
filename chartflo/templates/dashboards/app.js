function loadDashboard(page, dashboard, destination) {
	var url = "/dashboards/page/"+dashboard+"/"+page+"/";
	console.log("Getting", url);
	var spinner = '<div class="text-center" style="width:100%;margin-top:5em;opacity:0.6">';
	spinner = spinner + '<i class="fa fa-spinner fa-spin fa-5x fa-fw"></i>\n</div>';
	if ( destination === undefined) {
    	destination = "#content"
	}
	$(destination).html(spinner);
	axios.get(url).then(function (response) {
		$(destination).html(response.data);
	}).catch(function (error) {
		console.log(error);
	});
	$(".sparkline-embeded").each(function () {
		//console.log("LOAD");
		var $this = $(this);
		$this.sparkline('html', $this.data());
		console.log($this.data())
	});
}

$(document).ready(function () {
	loadDashboard("index", "{{ dashboard }}");
	$(".sparkline").each(function () {
		//console.log("INIT");
		var $this = $(this);
		$this.sparkline('html', $this.data());
		console.log($this.data())
	});
});