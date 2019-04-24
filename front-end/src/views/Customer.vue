<template>
  <div>
    <div v-for="customer in customers" :key="customer.id">
      <Customer :customer="customer"></Customer>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import Customer from "@/components/Customer.vue";

export default {
  name: "customer",
  components: {
    Customer
  },
  mounted() {
    this.$store.dispatch("loadCustomers");
  },
  computed: mapState(["customers"])
};
</script>
