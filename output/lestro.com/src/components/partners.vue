<template>
  <div class="partners">
		<div class="partners__container">
			<div class="partners__slider__wrap">

				<div class="partners__nav">
					<ul class="partners__nav__list">
						<li @click='changeNav(0)' :key='"partList" + 0' :class='{is_active: 0 == activeSlide}' class="partners__nav__item" v-html="$t('brandsTitle')"></li>
						<li @click='changeNav(1)' :key='"partList" + 1' :class='{is_active: 1 == activeSlide}' class="partners__nav__item" v-html="$t('agenciesTitle')"></li>
					</ul>
				</div>

				<div class="partners__slider">
					<slick @beforeChange="handleBeforeChange" ref="partnersSlick" :options='slickOptions'>
						<div v-for='(slide, slideIndex) in partnersSlider' :key='"slideIndex" + slideIndex' class="partners__slide">
							<div v-for='(img, indexImg) in slide' :key='"img" + indexImg' class="partners__slide__logo">
								<img :src='img' alt="company logos">
							</div>
						</div>
					</slick>
				</div>

			</div>
		</div>
  </div>
</template>

<script>
import Slick from 'vue-slick';

export default {
  name: 'partners',
	components: {
		Slick 
	},
  data() {
		return {
			navList: [this.$t('brandsTitle'), this.$t('agenciesTitle')],
			slickOptions: {
				slidesToShow: 1,
				dots: false,
				arrows: false,
				infinite: false,
				adaptiveHeight: true,
			
			},
			partnersSlider: [
				[
					'img/logo_1.svg',
					'img/logo_2.svg',
					'img/logo_3.svg',
					'img/logo_4.svg',
					'img/logo_5.svg',
					'img/logo_6.svg',
					'img/logo_7.svg',
					'img/logo_8.svg',
					'img/logo_9.svg',
					'img/logo_10.svg',
					'img/logo_11.svg',
					'img/logo_12.svg',
					'img/logo_13.svg',
					'img/logo_14.svg',
					'img/logo_15.svg',
					'img/logo_16.svg',
					'img/logo_17.svg',
					'img/logo_18.svg',
				],
				[
					'img/logo_19.svg',
					'img/logo_20.svg',
					'img/logo_21.svg',
					'img/logo_22.svg',
					'img/logo_23.svg',
					'img/logo_24 1.svg',
					'img/logo_25.svg',
					'img/logo_26.svg',
					'img/logo_27.svg',
					'img/logo_28.svg',
					'img/logo_29.svg',
					'img/logo_30.svg',
					'img/logo_31.svg',
					'img/logo_32.svg',
					'img/logo_33.svg',
					'img/logo_34.svg',
				]
			],
			activeSlide: 0,
		}
	},
	methods: {
		next() {
			this.$refs.partnersSlick.next();
		},

		prev() {
			this.$refs.partnersSlick.prev();
		},
		changeNav(event) {
			this.$refs.partnersSlick.goTo(event);
			this.activeSlide = event;
		},
		handleBeforeChange(event, slick, currentSlide, nextSlide) {
			this.activeSlide = nextSlide;
		
		},
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">

</style>
