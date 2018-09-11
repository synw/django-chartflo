$(document).ready(function () {
	$('.datatable').DataTable();
	$(".sparkline").each(function () {
	  var $this = $(this);
	  $this.sparkline('html', $this.data());
	});
});
app.views = [
	{% for slug, title in views_titles.items %}
		{"slug": "{{ slug }}", "name": "{{ title }}"}{% if not forloop.last %},{% endif %}
	{% endfor %}
];
app.activeView= "{{ active_view }}";