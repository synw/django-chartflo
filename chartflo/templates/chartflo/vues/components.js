help: {
	data: function() {
        return {
            isActive: false
        }
    },
	props: ["text"],
	template: `<span>
				<a v-on:click="isActive=!isActive">
				<span class="icon has-text-grey-light">
					<i class="fas fa-question-circle"></i>
				</span>
				</a>
				<div class="notification" v-if="isActive===true" style="margin-top:1em;font-size:80% !important">
					<button class="delete" @click="isActive=false"></button>
					{% verbatim %}{{ text }}{% endverbatim %}
				</div>
				</span>
				`,
},