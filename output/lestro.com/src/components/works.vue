<template>
	<div class="works">
		<div class="works__container">
			<div v-for='(letter, index) in letters' :key='index' class="works__block nonemouse">
				<div @mouseenter='hoverOnCase' @mouseleave='leaveOutCase' :data-letter='index' :class='{white: typeof(letterHovered) == "string", is_hovered: letterHovered == index}' class="works__letter nonemouse">
					<a :href='letter.rel'>
						<p v-html='letter.letter'></p>
						<div class="works__case">
							<p class="works__case__title" v-html='letter.title'></p>
							<p class="works__case__p">look case</p>
						</div>
					</a>
				</div>
			</div>

			<a href="https://lestro.com/LESTRO_PRESENTATION.pdf">
			<div class="works__block">
				<div class="works__text" :class='{white: typeof(letterHovered) == "string"}'>
					 
						<div class="works__text__container"></div>
						<p class="works__text__title">{{ $t('presentationTitle') }}</p>
						<img src="../assets/images/down.svg" alt="left" class="works__text__arrow">
					
				</div>
			</div></a>
			
			<div class="works__bg" :class='{is_hovered: typeof(letterHovered) == "string"}'>
				<div v-for='(source, index) in sources' :key='"img" + index'>
					<img v-if='source.split("/")[1] == "img"' :data-src='source' class="works__bg__img-wr" :class='{is_hovered: letterHovered == index}' :alt='"case " + index'>
					<video v-if='source.split("/")[1] == "video"' :data-src='source' :class='{is_hovered: letterHovered == index}'>
						<source :data-src='source' type='video/mp4'>
					</video>
				</div>
			</div>

		</div>
	</div>
</template>

<script>
import {EventBus} from '../EventBus.js';

export default {
	name: 'works',
	data () {
		return {
			letters: [
				{
					letter: 'w',
					rel: '/w',
					title: 'Loreal'
				},
				{
					letter: 'o',
					rel: '/o',
					title: 'Saint Daniel'
				},
				{
					letter: 'r',
					rel: '/r',
					title: 'AVK'
				},
				{
					letter: 'k',
					rel: '/k',
					title: 'Pepsi'
				},
				{
					letter: 's',
					rel: '/s',
					title: 'Leroy Merlin'
				}
			],
			letterHovered: null,
			sources: [
				'./img/project_01.jpg',
				'./video/loop.mp4',
				'./img/project_03.jpg',
				'./img/project_04.jpg',
				'./img/project_05.jpg'
			]
		}
	},
	methods: {
		hoverOnCase(e) {
			this.letterHovered = e.target.dataset.letter;
			if(this.letterHovered == 1){
				document.querySelector('.works__bg video').play();
			}

			EventBus.$emit('letter-hovered', {hovered: true});
		},
		leaveOutCase() {
			this.letterHovered = null;
			if(this.letterHovered == 1){
				document.querySelector('.works__bg video').pause();
			}

			EventBus.$emit('letter-hovered', {hovered: false});
		}
	}
}
</script>


<style lang="scss">

</style>
