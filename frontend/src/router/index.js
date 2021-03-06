import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);
import Profile from '../views/Profile.vue';
import Samples from '../views/Samples.vue';
import AllSamples from '../views/AllSamples.vue';
import Variants from '../views/Variants.vue';
import AllVariants from '../views/AllVariants.vue';
import Control from '../views/Control.vue';

// temp?
import login from '../views/LoginWorld.vue';


const routes = [
	{
		path: '/variants/:id',
		name: 'Variants',
		component: Variants,
		props: true
	},
	{
		path: '/allvariants',
		name: 'AllVariants',
		component: AllVariants,
		props: true
	},
	{
		path: '/samples',
		name: 'Samples',
		component: Samples
	},
	{
		path: '/allsamples',
		name: 'AllSamples',
		component: AllSamples
	},
	{
		path: '/control',
		name: 'Control',
		component: Control
	},
	{
		path: '/profile',
		name: 'Profile',
		component: Profile
	},
	{
		path: '/login',
		name: 'login',
		component: login
	},
	
];
const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
});
export default router;
