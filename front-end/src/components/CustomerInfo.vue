<script>
import { mapState } from 'vuex';
export default {
  // component setup
  name: "CustomerInfo",

  // component data
  computed: mapState(['selectedCustomer'])
};
</script>

<template>
  <div>{{ selectedCustomer }}</div>
</template>

<style scoped></style>
