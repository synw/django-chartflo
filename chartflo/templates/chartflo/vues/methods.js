isActiveBtn: function (slug) {
	if (slug === this.activeView) {
		return "is-link"
	} else {
		return ""
	}
},
isActiveView: function (slug) {
	if (slug === this.activeView) {
		return ""
	} else {
		return "hide"
	}
},
activateView: function(viewSlug) {
	this.activeView=viewSlug;
},