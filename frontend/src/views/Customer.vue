<script>
import { mapState } from "vuex";
import CustomerInfo from "@/components/CustomerInfo.vue";
import NewCustomerModal from "@/components/NewCustomerModal.vue";
import NewReportModal from "@/components/NewReportModal.vue";

export default {
  // component setup
  name: "customer",
  components: {
    CustomerInfo,
    NewCustomerModal,
    NewReportModal
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
    deleteSelectedCustomer() {
      this.$store.dispatch("deleteSelectedCustomer");
    },
    customerActive(customerId) {
      if (!this.selectedCustomer || customerId !== this.selectedCustomer.pk) {
        return false;
      }
      return true;
    },
    openNewCustomerModal() {
      this.$store.dispatch("toggleNewCustomerModal", true);
    },
    openNewReportModal() {
      this.$store.dispatch("toggleNewReportModal", true);
    }
  }
};
</script>

<template>
  <div>
    <!-- header row -->
    <div class="row mb-3">
      <!-- search bar -->
      <div class="col-4">
        <b-input-group>
          <!-- search area -->
          <b-form-input placeholder="Search customers..."></b-form-input>
          <!-- search buttons -->
          <b-input-group-append>
            <b-button variant="primary">
              <font-awesome-icon icon="search" />
            </b-button>
          </b-input-group-append>
        </b-input-group>
      </div>
      <!-- customer options -->
      <div class="col">
        <!-- manage customers -->
        <b-button-group class="mr-3">
          <b-button @click="openNewCustomerModal()" variant="primary">
            <font-awesome-icon icon="user-plus" />
          </b-button>
          <b-button
            :disabled="selectedCustomer === null"
            @click="deleteSelectedCustomer()"
            variant="danger"
          >
            <font-awesome-icon icon="user-minus" />
          </b-button>
        </b-button-group>
        <!-- manage reports -->
        <b-button
          :disabled="selectedCustomer === null"
          @click="openNewReportModal()"
          variant="primary"
        >
          <font-awesome-icon icon="file" />
        </b-button>
      </div>
    </div>
    <!-- information row -->
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
            @click="selectCustomer(customer.pk)"
            :key="customer.pk"
            :active="customerActive(customer.pk)"
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

    <!-- modals -->
    <NewCustomerModal></NewCustomerModal>
    <NewReportModal></NewReportModal>
  </div>
</template>

<style scoped>
.no-focus:focus {
  outline: none;
}
</style>
