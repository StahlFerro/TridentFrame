import Vue from 'vue';
import App from './App.vue';
import './css/bulmamods.css';
import './css/fontawesome-all.css'
// import { Plugin } from 'vue-fragment'

Vue.config.devtools = true;
// Vue.use(Plugin);

new Vue({
  el: '#app',
  render: h => h(App),
});
