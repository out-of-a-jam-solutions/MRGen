// vue stuff
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

// bootstrap
import BootstrapVue from "bootstrap-vue";
import "./scss/custom.scss";
Vue.use(BootstrapVue);

// font awesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faUserPlus,
  faUserMinus,
  faSearch,
  faCalendarMinus,
  faCalendarPlus,
  faFile,
  faTrashAlt
} from "@fortawesome/free-solid-svg-icons";

library.add(faUserPlus);
library.add(faUserMinus);
library.add(faSearch);
library.add(faCalendarMinus);
library.add(faCalendarPlus);
library.add(faFile);
library.add(faTrashAlt);
Vue.component("font-awesome-icon", FontAwesomeIcon);

// vue cookies
Vue.use(require("vue-cookies"));

// main vue component
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
