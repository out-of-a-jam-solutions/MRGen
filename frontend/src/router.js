import Vue from "vue";
import Router from "vue-router";
import Customer from "./views/Customer.vue";
import store from "./store";

Vue.use(Router);

async function loginGuard(to, from, next) {
  // try the route navigation
  if (store.state.loggedIn) {
    next();
  }
  // check if the user has a cookie
  await store.dispatch("verifyLogin");
  // try the route navigation again
  if (store.state.loggedIn) {
    next();
  } else {
    next("/login");
  }
}

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      beforeEnter: loginGuard,
      name: "customer",
      component: Customer
    },
    {
      path: "/reports",
      beforeEnter: loginGuard,
      name: "report",
      component: () =>
        import(/* webpackChunkName: "report" */ "./views/Report.vue")
    },
    {
      path: "/login",
      name: "login",
      component: () =>
        import(/* webpackChunkName: "login" */ "./views/Login.vue")
    }
  ]
});
