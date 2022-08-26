<template>
	<div class="services">

		<slick ref="servicesSlick" :options='slickOptions' class="services__container">
			<div :key='"serv" + 0' class="services__block">
				<div class="services__block__wrapper">
					<div class="services__letter">
						<div class="bodymovin" :id='"bodymovin" + (1)'></div>
					</div>
					<div class="services__text">
						<h2 class="services__text__title" v-html="$t('services.designTitle')"></h2>
						<p class="services__text__subtitle" v-html="$t('services.designSubtitle')"></p>
						<ul class="services__text__list">
							<li v-for="(props, propIndex) in $t('services.designProps')" :key='"servProp" + propIndex' class="services__text__item" v-html='props'></li>
						</ul>
					</div>
				</div>
			</div>

			<div :key='"serv" + 1' class="services__block">
				<div class="services__block__wrapper">
					<div class="services__letter">
						<div class="bodymovin" :id='"bodymovin" + (2)'></div>
					</div>
					<div class="services__text">
						<h2 class="services__text__title" v-html="$t('services.devTitle')"></h2>
						<p class="services__text__subtitle" v-html="$t('services.devSubtitle')"></p>
						<ul class="services__text__list">
							<li v-for="(props, propIndex) in $t('services.devProps')" :key='"servProp" + propIndex' class="services__text__item" v-html='props'></li>
						</ul>
					</div>
				</div>
			</div>

			<div :key='"serv" + 2' class="services__block">
				<div class="services__block__wrapper">
					<div class="services__letter">
						<div class="bodymovin" :id='"bodymovin" + 3'></div>
					</div>
					<div class="services__text">
						<h2 class="services__text__title" v-html="$t('services.supportTitle')"></h2>
						<p class="services__text__subtitle" v-html="$t('services.supportSubtitle')"></p>
						<ul class="services__text__list">
							<li v-for="(props, propIndex) in $t('services.supportProps')" :key='"servProp" + propIndex' class="services__text__item" v-html='props'></li>
						</ul>
					</div>
				</div>
			</div>
		</slick>

	</div>
</template>


<script>
import {EventBus} from '../EventBus.js';
import Slick from 'vue-slick';

export default {
	name: 'services',
	components: {
		Slick
	},
	data() {
		return {
			servicesInfo: [
				{
					animation: 'bodymoving1',
					title: this.$t('services.designTitle'),
					subtitle: this.$t('services.designSubtitle'),
					serviceProps: this.$t('services.designProps'),
				},
				{
					animation: 'bodymoving2',
					title: this.$t('services.devTitle'),
					subtitle: this.$t('services.devSubtitle'),
					serviceProps: this.$t('services.devProps'),
				},
				{
					animation: 'bodymoving3',
					title: this.$t('services.supportTitle'),
					subtitle: this.$t('services.supportSubtitle'),
					serviceProps: this.$t('services.supportProps'),
				}
			],
			slickOptions: {
				slidesToShow: 3,
				slidesToScroll: 3,
				arrows: false,
				infinite: false,
				responsive: [
					{
						breakpoint: 1023,
						settings: {
							slidesToShow: 1,
							slidesToScroll: 1,
							arrows: false,
							infinite: false,
							dots: true
						}
					}
				]
			},
			firstTime: true,
			positionName: 'hero'
		}
	},
	methods: {
		drawServicesLetters() {
			this.firstTime = false;
			let animateLetters = document.querySelectorAll('.bodymovin');
			animateLetters.forEach((letter, index) => {
				if(!letter.querySelector('.bodymovin svg')){
					let elementId = letter.getAttribute('id');
					let params = {
						container: letter,
						renderer: 'svg',
						loop: false,
						autoplay: true,
						path: (window.location.origin === "https://lestro.pages.git.lestro.com" ? window.location.origin + '/lestro-vue-markup' : window.location.origin) + '/json/' + elementId + '.json'
					};
					let anim;
					setTimeout(() => {
						anim = bodymovin.loadAnimation(params);
						document.querySelectorAll('.services__block')[index].classList.add('is_animated');
					}, 450 * index)
				}
			})
		}
	},
	mounted() {
		EventBus.$on('slide-changed', event => {
			if(event.next.anchor == 'services' && this.firstTime){
				setTimeout( _ => {
					this.drawServicesLetters();
				}, 500)
			}
		});
	}
}
</script>


<style lang="scss">
</style>