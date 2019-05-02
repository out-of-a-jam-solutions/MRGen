import Vue from "vue";
import Router from "vue-router";
import Customer from "./views/Customer.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "customer",
      component: Customer
    },
    {
      path: "/reports",
      name: "report",
      component: () =>
        import(/* webpackChunkName: "report" */ "./views/Report.vue")
    }
  ]
});
