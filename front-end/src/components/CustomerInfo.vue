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
  data() {
    return {
      form: {
        services: [],
        defaultCron: ["default-cron"],
        taskRunTime: "02:00"
      }
    };
  },
  computed: {
    // component methods
    ...mapState(["customers", "selectedCustomer", "schedules"]),

    // modal methods
    checkServicesValid() {
      return this.form.services.length >= 1;
    }
  },
  methods: {
    // component methods
    deleteSelectedCustomer() {
      this.$store.dispatch("deleteCustomer", [
        this.selectedCustomer.pk,
        this.customers.page
      ]);
    },

    // form methods
    submitForm() {
      // exit when the form isn't valid
      if (!this.validateForm()) {
        return false;
      }
      // parse the time form field
      const taskTime = this.form.taskRunTime.split(":");
      const hour = parseInt(taskTime[0]).toString();
      const minute = parseInt(taskTime[1]).toString();
      // submit the schedules
      for (const service of this.form.services) {
        const task = {
          minute: minute,
          hour: hour,
          day_of_week: "*",
          day_of_month: "*",
          month_of_year: "*"
        };
        this.$store.dispatch("createSchedule", [
          this.selectedCustomer.pk,
          service,
          task,
          this.schedules.page
        ]);
      }
      return true;
    },
    validateForm() {
      return true;
    },
    resetForm() {
      this.form = {
        services: [],
        defaultCron: ["default-cron"],
        taskRunTime: "02:00"
      };
    },
    toggleDefaultCron() {
      if (this.form.defaultCron.length === 0) {
        this.form.taskRunTime = "02:00";
      }
    },

    // modal methods
    handlePressOk(bvModalEvt) {
      // prevent modal from closing
      bvModalEvt.preventDefault();
      // trigger submit handler
      if (!this.submitForm()) {
        return;
      }
      // hide the modal manually
      this.$nextTick(() => {
        this.$refs.modal.hide();
      });
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
      <em slot="footer">
        <!-- edit the customer -->
        <b-button variant="primary" class="mr-2">
          Update customer
        </b-button>
        <!-- create new schedule -->
        <b-button
          @click="$bvModal.show('schedule-modal')"
          variant="primary"
          class="mr-2"
        >
          Add schedules
        </b-button>
        <!-- delete the customer -->
        <b-button
          @click="deleteSelectedCustomer()"
          variant="danger"
          class="mr-2"
        >
          Remove customer
        </b-button>
      </em>
    </b-card>

    <!-- schedule modal -->
    <b-modal
      @show="resetForm"
      @hidden="resetForm"
      @ok="handlePressOk"
      ref="modal"
      title="Add Schedules"
      id="schedule-modal"
    >
      <b-form @submit.stop.prevent>
        <!-- service selector -->
        <b-form-group label="Select services" label-for="service-selector">
          <b-form-checkbox-group id="service-selector" v-model="form.services">
            <!-- checkboxes -->
            <b-form-checkbox value="watchman">Watchman</b-form-checkbox>
            <b-form-checkbox value="repairshopr">RepairShopr</b-form-checkbox>
            <!-- validator feedback -->
            <b-form-invalid-feedback :state="checkServicesValid">
              Please select at least one
            </b-form-invalid-feedback>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group label="Schedule">
          <b-form-checkbox-group v-model="form.defaultCron" class="mb-2">
            <b-form-checkbox @change="toggleDefaultCron()" value="default-cron">
              Use default schedule
            </b-form-checkbox>
          </b-form-checkbox-group>
          <b-form-input
            v-model="form.taskRunTime"
            :disabled="form.defaultCron.length > 0"
            :type="'time'"
            placeholder="What time should the task run"
            id="cron-schedule"
            required
          >
          </b-form-input>
        </b-form-group>
      </b-form>
    </b-modal>
  </div>
</template>

<style scoped></style>
