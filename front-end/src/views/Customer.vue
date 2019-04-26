<script>
import { mapState } from "vuex";
import CustomerInfo from "@/components/CustomerInfo.vue";

export default {
  // component setup
  name: "customer",
  components: {
    CustomerInfo
  },

  // lifecycle hooks
  mounted: function() {
    this.$store.dispatch("loadCustomers");
  },

  // component data
  data: function() {
    return {
      CUSTOMERS_PER_PAGE: 10,
      SCHEDULES_PER_PAGE: 5
    };
  },
  computed: {
    // set the vuex state
    ...mapState(["customers", "selectedCustomer"]),
    // getter and setter for current customer page
    currentPage: {
      get() {
        return this.customers.page;
      },
      set(pageNumber) {
        this.$store.dispatch("loadCustomers", pageNumber);
      }
    }
  },
  methods: {
    selectCustomer(customerId) {
      this.$store.dispatch("selectCustomer", customerId);
    },
    customerActive(customerId) {
      if (!this.selectedCustomer || customerId !== this.selectedCustomer.pk) {
        return false;
      }
      return true;
    }
  }
};
</script>

<template>
  <div class="row">
    <div class="col-4">
      <!-- customer pagination bar -->
      <b-pagination
        v-if="customers.page_count > 1"
        v-model="currentPage"
        :total-rows="customers.results_count"
        :per-page="customers.page_size"
        align="fill"
        size="sm"
      ></b-pagination>
      <!-- customer list -->
      <b-list-group>
        <b-list-group-item
          v-for="customer in customers.results"
          :key="customer.pk"
          :active="customerActive(customer.pk)"
          @click="selectCustomer(customer.pk)"
          class="no-focus"
          button
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

<style scoped>
.no-focus:focus {
  outline: none;
}
</style>
