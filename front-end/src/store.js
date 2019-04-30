import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex);
Vue.use(VueAxios, axios);

export default new Vuex.Store({
  state: {
    customers: {},
    selectedCustomer: null,
    schedules: {},
    DEFAULT_CUSTOMERS_PER_PAGE: 10,
    DEFAULT_SCHEDULES_PER_PAGE: 10
  },
  mutations: {
    SET_CUSTOMERS(state, customers) {
      state.customers = customers;
    },
    SET_CURRENT_CUSTOMER(state, customer) {
      state.selectedCustomer = customer;
    },
    SET_SCHEDULES(state, schedules) {
      state.schedules = schedules;
    }
  },
  actions: {
    loadCustomers({ commit, state }, startingPage = 1) {
      // construct the pagination query parameters for the request
      const parameters = {
        params: {
          page: startingPage,
          page_size: state.DEFAULT_CUSTOMERS_PER_PAGE
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
    selectCustomer({ commit, state, dispatch }, customerId) {
      // attempt to load the customer
      const customer = state.customers.results.find(c => c.pk === customerId);
      // check if the customer is loaded
      if (customer === null) {
        return;
      }
      // select the customer
      commit("SET_CURRENT_CUSTOMER", customer);
      // load the customers schedules
      dispatch("loadSchedules", [customerId]);
    },
    loadSchedules({ commit, state }, [customerId, startingPage = 1]) {
      // construct the pagination query parameters for the request
      const parameters = {
        params: {
          page: startingPage,
          page_size: state.DEFAULT_SCHEDULES_PER_PAGE,
          customer: customerId
        }
      };
      // request the schedules from the server
      axios
        .get("http://localhost:8000/api/schedule", parameters)
        .then(r => r.data)
        .then(schedules => {
          commit("SET_SCHEDULES", schedules);
        });
    },
    deleteCustomer({ dispatch }, [customerId, startingPage]) {
      // delete the customer from the server
      axios
        .delete("http://localhost:8000/api/customer/" + customerId)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted customers from the back-end
          dispatch("loadCustomers", [customerId, startingPage]);
        });
    },
    deleteSchedule({ dispatch }, [scheduleId, startingPage]) {
      // delete the schedule from the server
      axios
        .delete("http://localhost:8000/api/schedule/" + scheduleId)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted schedules from the back-end
          dispatch("loadSchedules", [scheduleId, startingPage]);
        });
    }
  }
});
