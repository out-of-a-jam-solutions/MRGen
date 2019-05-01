<script>
import { mapState } from "vuex";
export default {
  // component setup
  name: "NewCustomerModal",

  // component data
  data() {
    return {
      name: "",
      watchmanId: null,
      repairshoprid: null
    };
  },
  methods: {
    modalClosed(submit = false) {
      // submit the form if submit is true
      if (submit) {
        this.submitForm();
      }
      // mark the modal as closed
      this.$store.dispatch("toggleNewCustomerModal", false);
    },
    submitForm() {
      console.log("SUBMIT FORM");
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
      @ok="modalClosed(true)"
      @hidden="modalClosed()"
      title="New Customer"
      id="new-customer-modal"
    >
    </b-modal>
  </div>
</template>

<style scoped></style>
