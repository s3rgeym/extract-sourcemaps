<template>
  <div id="app" class='app' :class='{bg_active3: activeSlide == 0 && lastSlide == 3, bg_active2: activeSlide == 0 && lastSlide == 2, bg_active: (activeSlide == 0 && lastSlide == 0 && mainPage) || (activeSlide == 0 && lastSlide == 1 && mainPage), bg_delay2: activeSlide == 2, bg_delay3: activeSlide == 3, bg_delay1: activeSlide == 1}'>
		<navigation></navigation>
		<achors></achors>
		<transition name="slide-in">
    	<router-view/>
		</transition>
		<contacts></contacts>
  </div>
</template>

<script>
import navigation from '@/components/navigation.vue';
import achors from '@/components/achors.vue';
import contacts from '@/components/contacts.vue';
import {EventBus} from '@/EventBus.js';

export default {
	name: 'app',
	data() {
		return {
			activeSlide: 0,
			lastSlide: 0,
			mainPage: true,
		}
	},
  components: {
		navigation,
		achors,
		contacts
	},
	watch: {
		'$route' (to, from) {
			const toDepth = to.path.split('/').length
			const fromDepth = from.path.split('/').length
			this.transitionName = toDepth < fromDepth ? 'slide-out' : 'slide-in'
		}
	},
	methods: {
		// navigation background on init page
		navBgOninit(index) {
			if(index != 3) {
				document.querySelector('.line__yellow').style.height = (document.querySelectorAll('.navigation__nav__item')[index]).getBoundingClientRect().bottom + 'px';
			} else if(window.innerWidth > 767){
				document.querySelector('.line__yellow').style.height = '100%';
			}
		}
	},
	created() {
		// on index page look at bg
		EventBus.$on('slide-changed', event => {
			this.lastSlide = event.cur.index;
			this.activeSlide = event.next.index;
			this.navBgOninit(event.next.index);
		});

		// look for background init
		EventBus.$on('on-main-page', event => {
			this.mainPage = event.status;
			this.activeSlide = event.sliderActiveIndex;
			this.lastSlide = event.sliderActiveIndex;
		});

	}
}
</script>


<style lang="scss">
/* @import '~/node_modules/slick-carousel/slick/slick.css'; */
@import "~@/assets/styles/main";

// animation for routing
.slide-in-enter-active {
  transition: transform .5s ease .5s, opacity	.3s ease .25s;
}
.slide-in-leave-active {
  transition: transform .8s cubic-bezier(1.0, 0.5, 0.8, 1.0), opacity	.3s ease .25s;
}
.slide-in-enter, .slide-in-leave-to{
  transform: translateX(100%);
  opacity: 0;
}


.slide-out-enter-active {
  transition: transform .5s ease .5s, opacity	.3s ease .25s;
}
.slide-out-leave-active {
  transition: transform .8s cubic-bezier(1.0, 0.5, 0.8, 1.0), opacity	.3s ease .25s;
}
.slide-out-enter, .slide-out-leave-to{
  transform: translateX(-100%);
  opacity: 0;
}


</style>
