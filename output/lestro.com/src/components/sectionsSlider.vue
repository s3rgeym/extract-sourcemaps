<template>
	<div class="sections">
		<full-page :options="options2" id="fullpage__content" ref="fullpage__content" class="section__wrapper">
			<div v-for='(section, index) in sections' :key='index' :class='section' class="section">
				<div class="container">
					<letters v-if='section == "section__hero"'></letters>
					<services v-if='section == "section__services"'></services>
					<works v-if='section == "section__works"'></works>
					<partners v-if='section == "section__partners"'></partners>
				</div>
			</div>
		</full-page>
	</div>
</template>


<script>
import letters from '@/components/letters.vue';
import services from '@/components/services.vue';
import works from '@/components/works.vue';
import partners from '@/components/partners.vue';
import {EventBus} from '../EventBus.js';

export default {
  name: 'sectionsSlider',
  components: {
		letters,
		services,
		works,
		partners,
	},
	data() {
		return {
			sections: ['section__hero', 'section__services', 'section__works', 'section__partners'],
			options2: {
				scrollOverflow: false,
				scrollBar: false,
				css3: true,
				touchSensitivity: 15,
				scrollingSpeed: 1000,
				licenseKey: 'OPEN-SOURCE-GPLV3-LICENSE',
				navigation: false,
				easing: 'ease',
				menu: '.js-navigation__list',
				anchors: ['hero', 'services', 'works', 'partners'],
				scrollOverflow: true,
				onLeave: this.onLeave,
			},
		}
	},
	methods: {
		onLeave(cur,next,way) {
			// event on change fp slide
			EventBus.$emit('slide-changed', {cur, next});
		}
	}
}
</script>


<style lang="scss">
</style>
