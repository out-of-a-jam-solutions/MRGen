<script>
import { mapState } from "vuex";
export default {
  name: "app",
  computed: {
    ...mapState(["loggedIn"])
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
    }
  }
}
</script>

<template>
  <div id="app">
    <b-navbar type="dark" variant="primary" class="mb-3">
      <!-- navbar title -->
      <b-navbar-brand href="#">MRGen</b-navbar-brand>
      <!-- navbar content -->
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">Customers</b-nav-item>
          <b-nav-item to="/reports">Reports</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item v-if="loggedIn" @click="logout()" to="/login" right>Logout</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>
