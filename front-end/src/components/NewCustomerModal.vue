<script>
import { mapState } from "vuex";
export default {
  // component setup
  name: "NewCustomerModal",

  // lifecycle hooks
  mounted: function() {
    this.resetForm();
  },

  // component data
  data() {
    return {
      form: {
        name: "",
        watchmanId: null,
        repairshoprId: null
      },
      nameState: null
    };
  },
  methods: {
    modalSubmit(bvModalEvt) {
      // prevent modal from closing
      bvModalEvt.preventDefault();
      // submit the form if submit is true or else keep the modal open
      if (this.validateForm()) {
        this.submitForm();
      } else {
        return;
      }
      // hide the modal manually
      this.$nextTick(() => {
        this.$refs.modal.hide();
      });
      // modal close cleanup
      this.modalClosed();
    },
    modalClosed() {
      // mark the modal as closed
      this.$store.dispatch("toggleNewCustomerModal", false);
      // reset the form
      this.resetForm();
    },
    submitForm() {
      // set the watchman id and repairshopr id to null if they are blank
      if (this.form.watchmanId === "") {
        this.form.watchmanId = null;
      }
      if (this.form.repairshoprId === "") {
        this.form.repairshoprId = null;
      }
      // send the request to create the customer
      this.$store.dispatch("createCustomer", [
        this.form.name,
        this.form.watchmanId,
        this.form.repairshoprId
      ]);
    },
    validateForm() {
      // check if the form is valid
      const valid = this.$refs.form.checkValidity();
      // set the valid state variables
      this.nameState = valid ? "valid" : "invalid";
      return valid;
    },
    resetForm() {
      // reset the form
      this.form = {
        name: "",
        watchmanId: null,
        repairshoprId: null
      };
      // reset the state
      this.nameState = null;
    }
  },
  computed: mapState(["newCustomerModalOpen"]),
  watch: {
    newCustomerModalOpen(newValue) {
      // open the modal if the open value is set true
      if (newValue === true) {
        this.$bvModal.show("new-customer-modal");
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
      title="New Customer"
      ref="modal"
      id="new-customer-modal"
    >
      <b-form @submit.stop.prevent="validateForm" ref="form">
        <!-- customer name -->
        <b-form-group
          :state="nameState"
          label="Name"
          label-for="customer-name"
          invalid-feedback="Name is required"
        >
          <b-form-input
            v-model="form.name"
            :state="nameState"
            id="customer-name"
            required
          >
          </b-form-input>
        </b-form-group>
        <!-- watchman id -->
        <b-form-group label="Watchman ID" label-for="watchman-id">
          <b-form-input
            v-model="form.watchmanId"
            placeholder="optional"
            id="watchman-id"
          >
          </b-form-input>
        </b-form-group>
        <!-- repairshopr id -->
        <b-form-group label="RepairShopr ID" label-for="repairshopr-id">
          <b-form-input
            v-model="form.repairshoprId"
            placeholder="optional"
            id="watchman-id"
          >
          </b-form-input>
        </b-form-group>
      </b-form>
    </b-modal>
  </div>
</template>

<style scoped></style>
