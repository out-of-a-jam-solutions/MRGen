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
  <div v-if="selectedCustomer">
    <b-card
      :title="selectedCustomer.name"
      :sub-title="selectedCustomer.pk"
    >
      <b-card-text>
        Customer information
      </b-card-text>
    </b-card>
  </div>
</template>

<style scoped></style>
