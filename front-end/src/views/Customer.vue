<template>
  <div>
    <!-- customer list -->
    <div class="col-3">
      <!-- next customer page -->
      <b-button
        @click="nextPage()"
        :disabled="!customers.next"
      >
        Next Page
      </b-button>
      <!-- previous customer page -->
      <b-button
        @click="previousPage()"
        :disabled="!customers.previous"
      >
        Previous Page
      </b-button>
      <b-list-group>
        <b-list-group-item
          v-for="customer in customers.results"
          :key="customer.id"
          button
          class="no-focus"
        >
          {{ customer.name }}
        </b-list-group-item>
      </b-list-group>
    </div>
    <!-- customer information -->
    <div class="col">
      <CustomerInfo></CustomerInfo>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import Customer from "@/components/Customer.vue";
import CustomerInfo from "@/components/CustomerInfo.vue";

export default {
  name: "customer",
  components: {
    Customer,
    CustomerInfo
  },
  mounted() {
    const CUSTOMERS_PER_PAGE = 10;
    this.$store.dispatch("loadCustomers", [CUSTOMERS_PER_PAGE]);
  },
  computed: mapState(["customers"]),
  props: {
    nextDisabled: Boolean,
    previousDisabled: Boolean
  },
  methods: {
    nextPage: function() {
      this.$store.dispatch("nextPageCustomers");
    },
    previousPage: function() {
      this.$store.dispatch("previousPageCustomers");
    }
  }
};
</script>

<style scoped>
.no-focus:focus {
  outline: none;
}
</style>
