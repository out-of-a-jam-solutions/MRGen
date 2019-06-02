<script>
import { mapState } from "vuex";
export default {
  name: "login",
  mounted: function() {
    this.$store.dispatch("verifyLogin");
  },
  computed: {
    ...mapState(["loggedIn"])
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.$store
        .dispatch("loginUserPass", [this.form.username, this.form.password])
        .then(() => {
          this.$router.push("/");
        })
        .catch(error => {
          this.$bvToast.toast(error.response.data.detail, {
            title: "Login Failed!",
            variant: "danger",
            solid: true
          });
        });
    }
  },
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  }
};
</script>

<template>
  <div>
    <h1>Login</h1>
    <b-form v-if="!loggedIn" @submit="onSubmit">
      <!-- username -->
      <b-form-group id="username-group" label="Username" label-for="username">
        <b-form-input
          v-model="form.username"
          id="username"
          required
        ></b-form-input>
      </b-form-group>
      <!-- password -->
      <b-form-group label="Password" label-for="password" id="password-group">
        <b-form-input
          v-model="form.password"
          type="password"
          id="password"
          required
        ></b-form-input>
      </b-form-group>
      <!-- login button -->
      <b-button type="submit" variant="primary">Login</b-button>
    </b-form>
    <p v-else>Your are already logged in!</p>
  </div>
</template>

<style scoped></style>
