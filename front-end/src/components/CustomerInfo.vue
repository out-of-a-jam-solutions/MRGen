<script>
import { mapState } from "vuex";

export default {
  // component setup
  name: "CustomerInfo",

  // component data
  computed: {
    ...mapState([
      "customers",
      "selectedCustomer",
      "schedules",
      "DEFAULT_SERVICES"
    ]),
    selectedServices: {
      get: function() {
        return this.schedules.results.map(x => x.task_type);
      },
      set: function(newServices) {
        // check for deletions
        for (const service of this.selectedServices) {
          if (!newServices.includes(service)) {
            this.deleteScheduleByTaskType(service);
          }
        }
        // check for additions
        for (const service of newServices) {
          if (!this.selectedServices.includes(service)) {
            this.$store.dispatch("createSchedule", [
              this.selectedCustomer.pk,
              service
            ]);
          }
        }
      }
    }
  },
  methods: {
    getServiceName(service) {
      // correctly create known services
      if (service === "repairshopr") {
        return "RepairShopr";
      } else if (service === "watchman") {
        return "Watchman Monitoring";
      }
      // default fallback
      else {
        return service.charAt(0).toUpperCase() + service.slice(1);
      }
    },
    deleteScheduleByTaskType(taskType) {
      // delete all schedules where the task type matches
      for (const schedule of this.schedules.results) {
        if (schedule.task_type === taskType) {
          // make a request to delete the task
          this.$store.dispatch("deleteSchedule", [schedule.pk]);
        }
      }
    }
  }
};
</script>

<template>
  <div v-if="selectedCustomer">
    <!-- customer info -->
    <b-card :title="selectedCustomer.name">
      <!-- customer information -->
      <h5 class="mt-3">Customer Information</h5>
      <b-card-text>
        MRGen ID: {{ selectedCustomer.pk }}
        <br />
        Watchman ID: {{ selectedCustomer.watchman_group_id }}
        <br />
        RepairShopr ID: {{ selectedCustomer.repairshopr_id }}
      </b-card-text>
      <!-- services -->
      <h5>Services</h5>
      <b-form>
        <b-form-group>
          <b-form-checkbox-group v-model="selectedServices" stacked>
            <b-form-checkbox
              v-for="service of DEFAULT_SERVICES"
              :key="service"
              :value="service"
            >
              {{ getServiceName(service) }}
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
      </b-form>
    </b-card>
  </div>
</template>

<style scoped></style>
