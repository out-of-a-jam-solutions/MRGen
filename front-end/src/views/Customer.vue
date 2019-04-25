<template>
  <div class="row">
    <div class="col-4">
      <!-- customer pagination bar -->
      <b-pagination
        v-if="customers.page_count > 1"
        v-model="currentPage"
        :total-rows="customers.results_count"
        :per-page="customers.page_size"
        @input="changePage()"
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

<script>
import { mapState } from "vuex";
import CustomerInfo from "@/components/CustomerInfo.vue";

export default {
  name: "customer",
  components: {
    CustomerInfo
  },
  mounted() {
    this.$store.dispatch("loadCustomers", [this.CUSTOMERS_PER_PAGE]);
  },
  computed: mapState(["customers"]),
  methods: {
    changePage: function() {
      this.$store.dispatch("loadCustomers", [
        this.CUSTOMERS_PER_PAGE,
        this.currentPage
      ]);
    }
  },
  data: function() {
    return {
      CUSTOMERS_PER_PAGE: 10,
      currentPage: 1
    };
  }
};
</script>

<style scoped>
.no-focus:focus {
  outline: none;
}
</style>
