<script>
import { mapState } from "vuex";
import Schedule from "@/components/Schedule.vue";

export default {
  // component setup
  name: "CustomerInfo",
  components: {
    Schedule
  },

  // component data
  computed: mapState(["customers", "selectedCustomer", "schedules"]),
  methods: {
    deleteSelectedCustomer() {
      this.$store.dispatch('deleteCustomer', [this.selectedCustomer.pk, this.customers.page]);
    }
  }
};
</script>

<template>
  <div v-if="selectedCustomer">
    <b-card
      :title="selectedCustomer.name"
    >
      <!-- customer information -->
      <h5 class="mt-3">Customer Information</h5>
      <b-card-text>
        MRGen ID: {{ selectedCustomer.pk }}
        <br/>
        Watchman ID: {{ selectedCustomer.watchman_group_id }}
        <br/>
        RepairShopr ID: {{ selectedCustomer.repairshopr_id }}
      </b-card-text>
      <!-- schedules -->
      <h5>Schedules</h5>
      <b-list-group>
        <Schedule
          v-for="schedule in schedules.results"
          :key="schedule.pk"
          :schedule="schedule"
        ></Schedule>
      </b-list-group>
      <!-- footer -->
      <em
        slot="footer"
      >
        <b-button
          variant="primary"
          class="mr-2"
        >
          Update customer
        </b-button>
        <b-button
          variant="primary"
          class="mr-2"
        >
          Update schedules
        </b-button>
        <b-button
          @click="deleteSelectedCustomer()"
          variant="danger"
          class="mr-2"
        >
          Remove customer
        </b-button>
      </em>
    </b-card>
  </div>
</template>

<style scoped></style>
