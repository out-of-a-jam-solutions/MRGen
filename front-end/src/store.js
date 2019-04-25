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
      axios
        .get("http://localhost:8000/api/customer", parameters)
        .then(r => r.data)
        .then(customers => {
          commit("SET_CUSTOMERS", customers);
        });
    },
    nextPageCustomers({ commit, state }) {
      // if a next page exists, get it
      if (state.customers.next) {
        axios
          .get(state.customers.next)
          .then(r => r.data)
          .then(customers => {
            commit("SET_CUSTOMERS", customers);
          });
      }
    },
    previousPageCustomers({ commit, state }) {
      // if a previous page exists, get it
      if (state.customers.previous) {
        axios
          .get(state.customers.previous)
          .then(r => r.data)
          .then(customers => {
            commit("SET_CUSTOMERS", customers);
          });
      }
    }
  }
});
