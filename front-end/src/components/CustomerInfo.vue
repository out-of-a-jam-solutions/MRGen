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
  data: function() {
    return {
      SCHEDULES_PER_PAGE: 10
    };
  },
  computed: mapState(["selectedCustomer", "schedules"]),
  methods: {
    subTitle(pk) {
      return "ID: " + pk;
    }
  }
};
</script>

<template>
  <div v-if="selectedCustomer">
    <b-card
      :title="selectedCustomer.name"
      :sub-title="subTitle(selectedCustomer.pk)"
    >
      <b-card-text>Schedules</b-card-text>
      <!-- schedules -->
      <b-list-group>
        <Schedule
          v-for="schedule in schedules.results"
          :key="schedule.pk"
          :schedule="schedule"
        ></Schedule>
      </b-list-group>
    </b-card>
  </div>
</template>

<style scoped></style>
