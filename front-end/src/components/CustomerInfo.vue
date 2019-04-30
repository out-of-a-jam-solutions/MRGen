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
      newServices: [],
      defaultCron: ["default-cron"],
      crontab: "0 2 * * *"
    };
  },
  computed: {
    ...mapState(["customers", "selectedCustomer", "schedules"]),
    checkServicesValid() {
      return this.newServices.length >= 1;
    }
  },
  methods: {
    useDefaultCron() {
      if (this.defaultCron.length === 0) {
        this.crontab = "0 2 * * *";
      } else {
        this.crontab = "";
      }
    },
    handleScheduleOk(bvModalEvt) {
      // prevent modal from closing
      bvModalEvt.preventDefault()
      // trigger submit handler
      this.handleSubmit()
    },
    handleSubmit() {
      // exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return
      }
      // push the name to submitted names
      // this.submittedNames.push(this.name)
      console.log("SUBMIT");
      // hide the modal manually
      this.$nextTick(() => {
        this.$refs.modal.hide()
      });
    },
    checkFormValidity() {
      console.log("CHECK VALIDITY");
      return true;
    },
    resetScheduleModal() {
      this.newServices = [];
      this.defaultCron = ["default-cron"];
      this.crontab = "0 2 * * *";
    },
    deleteSelectedCustomer() {
      this.$store.dispatch("deleteCustomer", [
        this.selectedCustomer.pk,
        this.customers.page
      ]);
    }
  }
};
</script>

<template>
  <div v-if="selectedCustomer">
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

    <!-- create schedule modal -->
    <b-modal
      @show="resetScheduleModal"
      @hidden="resetScheduleModal"
      @ok="handleScheduleOk"
      ref="modal"
      title="Add Schedules"
      id="schedule-modal"
    >
      <b-form>
        <!-- service selector -->
        <b-form-group label="Select services" label-for="service-selector">
          <b-form-checkbox-group id="service-selector" v-model="newServices">
            <!-- checkboxes -->
            <b-form-checkbox value="watchman">Watchman</b-form-checkbox>
            <b-form-checkbox value="repairshopr">RepairShopr</b-form-checkbox>
            <!-- validator feedback -->
            <b-form-invalid-feedback :state="checkServicesValid">
              Please select at least one
            </b-form-invalid-feedback>
          </b-form-checkbox-group>
        </b-form-group>
        <!-- watchman id -->
        <b-form-group label="Service IDs">
          <b-form-input
            v-if="newServices.includes('watchman')"
            placeholder="Enter the customer's Watchman ID"
            class="mb-2"
            required
          >
          </b-form-input>
          <b-form-input
            v-if="newServices.includes('repairshopr')"
            placeholder="Enter the customer's RepairShopr ID"
            class="mb-2"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group label="Schedule">
          <b-form-checkbox-group v-model="defaultCron" class="mb-2">
            <b-form-checkbox @change="useDefaultCron()" value="default-cron">
              Use default schedule
            </b-form-checkbox>
          </b-form-checkbox-group>
          <b-form-input
            v-model="crontab"
            :disabled="defaultCron.length > 0"
            placeholder="Enter a crontab schedule"
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
