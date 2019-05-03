// vue stuff
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

// bootstrap
import BootstrapVue from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);

// font awesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faUserPlus,
  faUserMinus,
  faSearch,
  faCalendarMinus,
  faCalendarPlus
} from "@fortawesome/free-solid-svg-icons";

library.add(faUserPlus);
library.add(faUserMinus);
library.add(faSearch);
library.add(faCalendarMinus);
library.add(faCalendarPlus);
Vue.component("font-awesome-icon", FontAwesomeIcon);

// main vue component
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
