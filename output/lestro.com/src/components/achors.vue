<template>
	<div class="achors">
		<div class="container container--abs">

			<div @click='backToPrevPage' :class='{is_hidden: position === 0 || openContacts, white: hoveredWorks, on_index: onMainPage}' class="achors__item achors__top">
				<p>
					{{ $t('back') }}
				</p>
				<img src="../assets/images/back.svg" alt="go back" class="svg">
			</div>
			<div @click='slideBottom' :class='{is_hidden: position === 3 || openContacts || !onMainPage, white: hoveredWorks }' class="achors__item achors__bottom">
				<p>
					{{ $t('down') }}
				</p>
				<img src="../assets/images/down.svg" alt="go bottom" class="svg">
			</div>

		</div>

		<div class="achors__item achors__contacts" :class='{white: hoveredWorks}'>
			<p v-show='!openContacts' @click='contactsClickEvent'>{{ $t('contactsTitle') }}</p>
			<p v-show='openContacts' @click='contactsClickEvent'>{{ $t('close') }}</p>
		</div>

		<div class="achors__item achors__fb" :class='{white: hoveredWorks}'>
			<a target="_blank" href="https://www.facebook.com/lestroweb/">
				<p>{{ $t('subscribe') }}</p>
				<img src="../assets/images/facebook.svg" alt="facebook">
			</a>
		</div>

	</div>
</template>


<script>
import {EventBus} from '../EventBus.js';

export default {
	name: 'achors',
	data() {
		return {
			position: 0,
			contacts: true,
			fb: true,
			hoveredWorks: false,
			openContacts: false,
			onMainPage: true,
		}
	},
	computed: {
	},
	methods: {
		backToPrevPage() {
			// need check for fb on site
			if((typeof(fullpage_api) != 'undefined') && this.onMainPage){
				fullpage_api.moveSectionUp();
			} else if(!this.onMainPage){
				window.history.back();
			}
		},
		slideBottom() {
			// need check for fb on site
			if(fullpage_api){
				fullpage_api.moveSectionDown();
			}
		},
		contactsClickEvent() {
			document.querySelector('body').classList.toggle('body-overflow');
			if(!this.openContacts){
				this.openContacts = true;
				if((typeof(fullpage_api) != 'undefined') && this.onMainPage){
					fullpage_api.setAllowScrolling(false)
				}
			} else {
				this.openContacts = false;
				if((typeof(fullpage_api) != 'undefined') && this.onMainPage){
					fullpage_api.setAllowScrolling(true)
				}
			}

			// click on contacts store
			EventBus.$emit('contacts-button-event', {status: this.openContacts});
		}
	},
	created() {
		// change slide on main page
		EventBus.$on('slide-changed', event => {
			this.position = event.next.index;
		});

		// hover event on index page on section works
		EventBus.$on('letter-hovered', event => {
			this.hoveredWorks = event.hovered;
		});

		// event when contacts button was clicked
		EventBus.$on('contacts-button-event', event => {
			this.openContacts = event.status;
		});

		// event when change to another page
		EventBus.$on('on-main-page', event => {
			this.onMainPage = event.status;
			
			if(!event.status){
				this.position = null;
			} else {
				this.position = event.sliderActiveIndex;
			}
			
		});
	}
}
</script>


<style lang="scss">
</style>
