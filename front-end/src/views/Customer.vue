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
    this.$store.dispatch("loadCustomers", [this.CUSTOMERS_PER_PAGE]);
  },

  // component data
  computed: {
    // set the vuex state
    ...mapState(["customers"]),
    // getter and setter for current customer page
    currentPage: {
      get() {
        return this.customers.page;
      },
      set(pageNumber) {
        this.$store.dispatch("loadCustomers", [
          this.CUSTOMERS_PER_PAGE,
          pageNumber
        ]);
      }
    }
  },
  data: function() {
    return {
      CUSTOMERS_PER_PAGE: 10
    };
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

<style scoped>
.no-focus:focus {
  outline: none;
}
</style>
