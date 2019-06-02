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
      "reports",
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
    },
    currentPage: {
      get() {
        return this.reports.page;
      },
      set(pageNumber) {
        this.$store.dispatch("loadReports", [
          this.selectedCustomer.pk,
          pageNumber
        ]);
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
          this.$store.dispatch("deleteSchedule", schedule.pk);
        }
      }
    },
    loadReport(reportId) {
      var link = `${
        process.env.VUE_APP_BACKEND_URL
      }/api/report/detail/${reportId}.pdf`;
      // open the selected report in a new window
      window.open(link);
    },
    deleteReport(reportId) {
      this.$store.dispatch("deleteReport", [reportId]);
    },
    disableService(service) {
      // returns true if the service is not null
      if (service === "repairshopr") {
        return this.selectedCustomer.repairshopr_id === null;
      } else if (service === "watchman") {
        return this.selectedCustomer.watchman_group_id === null;
      }
      return false;
    }
  },
  data() {
    return {
      reportDisplayFeilds: ["start_date", "end_date", "options"]
    };
  }
};
</script>

<template>
  <div v-if="selectedCustomer">
    <!-- customer info -->
    <b-card :title="selectedCustomer.name" class="mb-3">
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
              :disabled="disableService(service)"
            >
              {{ getServiceName(service) }}
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
      </b-form>
    </b-card>
    <!-- reports -->
    <b-card title="Reports" class="mb-3">
      <!-- reports pagination bar -->
      <b-pagination
        v-if="reports.page_count > 1"
        v-model="currentPage"
        :total-rows="reports.results_count"
        :per-page="reports.page_size"
        size="sm"
      ></b-pagination>
      <!-- reports table -->
      <b-table :items="reports.results" :fields="reportDisplayFeilds" fixed>
        <template slot="options" slot-scope="row">
          <b-button-group>
            <b-button
              @click="loadReport(row.item.pk)"
              variant="secondary"
              size="sm"
            >
              View PDF
            </b-button>
            <b-button @click="deleteReport(row.item.pk)" variant="danger">
              <font-awesome-icon icon="trash-alt" />
            </b-button>
          </b-button-group>
        </template>
      </b-table>
    </b-card>
  </div>
</template>

<style scoped></style>
