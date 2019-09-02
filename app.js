import Vue from 'vue';
import App from './App.vue';
import './css/bulmamods.css';
import './css/fontawesome-all.css'

Vue.config.devtools = true;

new Vue({
  el: '#app',
  render: h => h(App),
});
