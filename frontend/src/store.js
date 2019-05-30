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
    // reports
    reports: {
      results: []
    },
    newReportModalOpen: false,
    // defaults
    DEFAULT_CUSTOMERS_PER_PAGE: 10,
    DEFAULT_SCHEDULES_PER_PAGE: 10,
    DEFAULT_REPORTS_PER_PAGE: 10,
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
    },
    SET_REPORTS(state, reports) {
      state.reports = reports;
    },
    SET_NEW_REPORT_MODAL_OPEN(state, open) {
      state.newReportModalOpen = open;
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
      // load the customers schedules and reports
      dispatch("loadSchedules", customerId);
      dispatch("loadReports", [customerId]);
    },
    loadCustomers({ commit, state }, startingPage = null) {
      // keep the current page number if no page is given
      if (startingPage === null) {
        startingPage = state.customers.page;
      }
      // construct the pagination query parameters for the request
      const parameters = {
        params: {
          page: startingPage,
          page_size: state.DEFAULT_CUSTOMERS_PER_PAGE
        }
      };
      // request the customers from the server
      axios
        .get(`${process.env.VUE_APP_BACKEND_URL}/api/customer`, parameters)
        .then(r => r.data)
        .then(customers => {
          commit("SET_CUSTOMERS", customers);
        });
    },
    createCustomer(
      { commit, dispatch, state },
      [name, watchmanId, repairshoprId, select = false]
    ) {
      // create the request body
      const body = {
        name: name,
        watchman_group_id: watchmanId,
        repairshopr_id: repairshoprId
      };
      // send the POST request
      return axios
        .post(`${process.env.VUE_APP_BACKEND_URL}/api/customer`, body)
        .then(r => r.data)
        .then(customer => {
          // load in customers
          dispatch("loadCustomers", state.customers.results.page);
          if (select) {
            commit("SET_CURRENT_CUSTOMER", customer);
          }
        });
    },
    deleteCustomer({ dispatch, state }, [customerId, startingPage = null]) {
      // keep the current page number if no page is given
      if (startingPage === null) {
        startingPage = state.customers.page;
      }
      // delete the customer from the server
      axios
        .delete(`${process.env.VUE_APP_BACKEND_URL}/api/customer/${customerId}`)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted customers from the back-end
          dispatch("loadCustomers", startingPage);
        });
    },
    deleteSelectedCustomer({ dispatch, state }) {
      dispatch("deleteCustomer", [state.selectedCustomer.pk]);
    },
    toggleNewCustomerModal({ commit, state }, open = null) {
      if (open || open === false) {
        commit("SET_NEW_CUSTOMER_MODAL_OPEN", open);
      } else {
        commit("SET_NEW_CUSTOMER_MODAL_OPEN", !state.newCustomerModalOpen);
      }
    },

    // schedules
    loadSchedules({ commit, state }, customerId) {
      // construct the pagination query parameters for the request
      const parameters = {
        params: {
          // pagination for schedules will be removed, always use the first page
          page: 1,
          page_size: state.DEFAULT_SCHEDULES_PER_PAGE,
          customer: customerId
        }
      };
      // request the schedules from the server
      axios
        .get(`${process.env.VUE_APP_BACKEND_URL}/api/schedule`, parameters)
        .then(r => r.data)
        .then(schedules => {
          commit("SET_SCHEDULES", schedules);
        });
    },
    createSchedule(
      { dispatch, state },
      [customerId, taskType, periodicTask = null]
    ) {
      // use the default periodic task if none is given
      if (periodicTask === null) {
        periodicTask = state.DEFAULT_PERIODIC_TASK;
      }
      // request query params
      const body = {
        customer: customerId,
        task_type: taskType,
        periodic_task: periodicTask
      };
      // request to create new schedule
      axios
        .post(`${process.env.VUE_APP_BACKEND_URL}/api/schedule`, body)
        .then(r => r.data)
        .then(() => {
          // load in the customers from the back-end
          dispatch("loadSchedules", customerId);
        });
    },
    deleteSchedule({ dispatch, state }, scheduleId) {
      // delete the schedule from the server
      axios
        .delete(`${process.env.VUE_APP_BACKEND_URL}/api/schedule/${scheduleId}`)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted schedules from the back-end for the current customer
          dispatch("loadSchedules", state.selectedCustomer.pk);
        });
    },

    // reports
    loadReports({ commit, state }, [customerId, startingPage = null]) {
      // keep the current page number if no page is given
      if (startingPage === null) {
        startingPage = state.reports.page;
      }
      // construct the pagination query parameters for the request
      const parameters = {
        params: {
          customer: customerId,
          page: startingPage,
          page_size: state.DEFAULT_REPORTS_PER_PAGE
        }
      };
      // request the reports from the server
      axios
        .get(`${process.env.VUE_APP_BACKEND_URL}/api/report`, parameters)
        .then(r => r.data)
        .then(reports => {
          commit("SET_REPORTS", reports);
        });
    },
    createReport({ dispatch }, [customerId, startDate, endDate]) {
      // create the request body
      const body = {
        customer: customerId,
        start_date: startDate,
        end_date: endDate
      };
      // send the POST request
      return axios
        .post(`${process.env.VUE_APP_BACKEND_URL}/api/report`, body)
        .then(r => r.data)
        .then(() => {
          // load in reports
          dispatch("loadReports", [customerId]);
        });
    },
    deleteReport({ dispatch, state }, [reportId, startingPage = null]) {
      // keep the current page number if no page is given
      if (startingPage === null) {
        startingPage = state.reports.page;
      }
      // delete the customer from the server
      axios
        .delete(`${process.env.VUE_APP_BACKEND_URL}/api/report/${reportId}`)
        .then(r => r.data)
        .then(() => {
          // load in the non-deleted customers from the back-end
          dispatch("loadReports", [state.selectedCustomer.pk, startingPage]);
        });
    },
    toggleNewReportModal({ commit, state }, open = null) {
      if (open || open === false) {
        commit("SET_NEW_REPORT_MODAL_OPEN", open);
      } else {
        commit("SET_NEW_REPORT_MODAL_OPEN", !state.newReportModalOpen);
      }
    }
  }
});
