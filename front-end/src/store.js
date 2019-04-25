import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex);
Vue.use(VueAxios, axios);

export default new Vuex.Store({
  state: {
    customers: {}
  },
  mutations: {
    SET_CUSTOMERS(state, customers) {
      state.customers = customers;
    }
  },
  actions: {
    loadCustomers({ commit }, [itemsPerPage, startingPage = 1]) {
      // construct the pagination query parameters for the request
      const parameters = {
        params: {
          page: startingPage,
          page_size: itemsPerPage
        }
      };
      // request the customers from the server
      axios
        .get("http://localhost:8000/api/customer", parameters)
        .then(r => r.data)
        .then(customers => {
          commit("SET_CUSTOMERS", customers);
        });
    }
  }
});
