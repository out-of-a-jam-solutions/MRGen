<script>
import { mapState } from "vuex";
export default {
  // component setup
  name: "NewReportModal",

  // lifecycle hooks
  mounted: function() {
    this.resetForm();
  },

  // component data
  data() {
    return {
      form: {
        startDate: null,
        endDate: null
      }
    };
  },
  methods: {
    modalSubmit(bvModalEvt) {
      // prevent modal from closing
      bvModalEvt.preventDefault();
      // submit the form if submit is true or else keep the modal open
      if (!this.validateForm()) {
        return;
      }
      this.submitForm().then(() => {
        // hide the modal manually
        this.$nextTick(() => {
          this.$refs.modal.hide();
        });
        // modal close cleanup
        this.modalClosed();
      });
    },
    modalClosed() {
      // mark the modal as closed
      this.$store.dispatch("toggleNewReportModal", false);
      // reset the form
      this.resetForm();
    },
    submitForm() {
      return new Promise(resolve => {
        // send the request to create the report
        this.$store
          .dispatch("createReport", [
            this.selectedCustomer.pk,
            this.form.startDate,
            this.form.endDate
          ])
          .then(() => {
            resolve();
          });
      });
    },
    validateForm() {
      // check if the form is valid
      const valid = this.$refs.form.checkValidity();
      return valid;
    },
    resetForm() {
      // reset the form
      this.form = {
        startDate: null,
        endDate: null
      };
    }
  },
  computed: mapState(["selectedCustomer", "newReportModalOpen"]),
  watch: {
    newReportModalOpen(newValue) {
      // open the modal if the open value is set true
      if (newValue) {
        this.$bvModal.show("new-report-modal");
      }
    }
  }
};
</script>

<template>
  <div>
    <b-modal
      @ok="modalSubmit"
      @hidden="modalClosed"
      title="New Report"
      ref="modal"
      id="new-report-modal"
    >
      <b-form @submit.stop.prevent="validateForm" ref="form">
        <!-- start date -->
        <b-form-group
          label="Start date"
          label-for="start-date"
          invalid-feedback="A start date is required"
        >
          <b-form-input
            v-model="form.startDate"
            type="date"
            id="start-date"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="End date"
          label-for="end-date"
          invalid-feedback="An end date is required"
        >
          <b-form-input
            v-model="form.endDate"
            type="date"
            id="end-date"
            required
          >
          </b-form-input>
        </b-form-group>
      </b-form>
    </b-modal>
  </div>
</template>

<style scoped></style>
