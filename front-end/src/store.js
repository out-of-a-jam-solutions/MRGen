import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex);
Vue.use(VueAxios, axios);

export default new Vuex.Store({
  state: {
    // customers
    customers: {
      results: []
    },
    selectedCustomer: null,
    newCustomerModalOpen: false,
    // schedules
    schedules: {
      results: []
    },
    newScheduleModalOpen: false,
    // defaults
    DEFAULT_CUSTOMERS_PER_PAGE: 10,
    DEFAULT_SCHEDULES_PER_PAGE: 10,
    DEFAULT_SERVICES: ["watchman", "repairshopr"],
    DEFAULT_PERIODIC_TASK: {
      minute: "0",
      hour: "2",
      day_of_week: "*",
      day_of_month: "*",
      month_of_year: "*"
    }
  },
  mutations: {
    SET_CUSTOMERS(state, customers) {
      state.customers = customers;
    },
    SET_CURRENT_CUSTOMER(state, customer) {
      state.selectedCustomer = customer;
    },
    SET_NEW_CUSTOMER_MODAL_OPEN(state, open) {
      state.newCustomerModalOpen = open;
    },
    SET_SCHEDULES(state, schedules) {
      state.schedules = schedules;
    }
  },
  actions: {
    // customers
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
    createCustomer({ dispatch, state }, [name, watchmanId, repairshoprId]) {
      // create the request body
      const body = {
        name: name,
        watchman_group_id: watchmanId,
        repairshopr_id: repairshoprId
      };
      // send the POST request
      axios
        .post("http://localhost:8000/api/customer", body)
        .then(r => r.data)
        .then(() => {
          // load in customers
          dispatch("loadCustomers", state.customers.results.page);
        });
    },
    deleteCustomer({ dispatch }, [customerId, startingPage]) {
      // delete the customer from the server
      axios
        .delete("http://localhost:8000/api/customer/" + customerId)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted customers from the back-end
          dispatch("loadCustomers", startingPage);
        });
    },
    deleteSelectedCustomer({ dispatch, state }) {
      dispatch("deleteCustomer", [
        state.selectedCustomer.pk,
        state.customers.page
      ]);
    },
    toggleNewCustomerModal({ commit, state }, open = null) {
      if (open === true || open === false) {
        commit("SET_NEW_CUSTOMER_MODAL_OPEN", open);
      } else {
        commit("SET_NEW_CUSTOMER_MODAL_OPEN", !state.newCustomerModalOpen);
      }
    },

    // schedules
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
    createSchedule(
      { dispatch, state },
      [customerId, taskType, periodicTask = null]
    ) {
      if (periodicTask === null) {
        periodicTask = state.DEFAULT_PERIODIC_TASK;
      }
      const body = {
        customer: customerId,
        task_type: taskType,
        periodic_task: periodicTask
      };
      axios
        .post("http://localhost:8000/api/schedule", body)
        .then(r => r.data)
        .then(() => {
          // load in the customers from the back-end
          dispatch("loadSchedules", [customerId, state.schedules.page]);
        });
    },
    deleteSchedule({ dispatch, state }, [scheduleId, startingPage = null]) {
      if (startingPage === null) {
        startingPage = state.schedules.page;
      }
      // delete the schedule from the server
      axios
        .delete("http://localhost:8000/api/schedule/" + scheduleId)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted schedules from the back-end for the current customer
          dispatch("loadSchedules", [state.selectedCustomer.pk, startingPage]);
        });
    }
  }
});
