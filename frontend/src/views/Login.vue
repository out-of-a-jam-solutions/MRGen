<script>
export default {
  name: "login",
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.$store.dispatch("loginUserPass", [this.form.username, this.form.password]).then(() => {
        this.$router.push("/")
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
    <b-form @submit="onSubmit">
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
  </div>
</template>

<style scoped></style>
