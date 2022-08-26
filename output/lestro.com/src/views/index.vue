<template>
	<!-- <transition name="slide"> -->
		<main class="wrapper">
		<sectionsSlider ></sectionsSlider>
		</main>
	<!-- </transition> -->
</template>

<script>
// @ is an alias to /src
import sectionsSlider from '@/components/sectionsSlider.vue';
import {EventBus} from '../EventBus.js';

export default {
  name: 'index',
  components: {
		sectionsSlider,
	},
	methods: {
	},
	mounted() {
		// on init page, event index page 
		EventBus.$emit('on-main-page', {
			status: true, 
			sliderActiveIndex: null || Number(document.querySelector('.navigation__nav__item .active').parentNode.id),
		});
	}
}
</script>

<style lang="scss">
</style>
