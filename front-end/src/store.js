import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex);
Vue.use(VueAxios, axios);

export default new Vuex.Store({
  state: {
    customers: []
  },
  mutations: {
    SET_CUSTOMERS(state, customers) {
      state.customers = customers;
    }
  },
  actions: {
    loadCustomers({ commit }) {
      axios
        .get("http://localhost:8000/api/customer")
        .then(r => r.data.results)
        .then(customers => {
          commit("SET_CUSTOMERS", customers);
        });
    }
  }
});
