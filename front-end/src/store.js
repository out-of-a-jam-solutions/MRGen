import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex);
Vue.use(VueAxios, axios);

export default new Vuex.Store({
  state: {
    customers: {},
    selectedCustomer: null
  },
  mutations: {
    SET_CUSTOMERS(state, customers) {
      state.customers = customers;
    },
    SET_CURRENT_CUSTOMER(state, customer) {
      state.selectedCustomer = customer;
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
    },
    selectCustomer({ commit, state }, customerId) {
      // attempt to load the customer
      const customer = state.customers.results.find(c => c.pk === customerId);
      // check if the customer is loaded
      if (customer === null) {
        return;
      }
      // select the customer
      commit("SET_CURRENT_CUSTOMER", customer);
    }
  }
});
