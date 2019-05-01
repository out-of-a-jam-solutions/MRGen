<script>
import cronstrue from "cronstrue";
import { mapState } from "vuex";

export default {
  // component setup
  name: "Schedule",

  // component data
  props: {
    schedule: {
      type: Object,
      required: true
    }
  },
  computed: mapState(["schedules"]),
  methods: {
    parseCron(task) {
      const cronstring =
        task.minute +
        " " +
        task.hour +
        " " +
        task.day_of_week +
        " " +
        task.day_of_month +
        " " +
        task.month_of_year;
      return cronstrue.toString(cronstring, { verbose: true });
    },
    deleteSchedule() {
      this.$store.dispatch("deleteSchedule", [
        this.schedule.pk,
        this.schedules.page
      ]);
    }
  }
};
</script>

<template>
  <b-list-group-item>
    <div class="row">
      <!-- schedule info -->
      <div class="col">
        Task Type: {{ schedule.task_type }}
        <br />
        Run schedule: {{ parseCron(schedule.periodic_task) }}
      </div>
      <!-- buttons -->
      <div class="col-2">
        <b-button
          @click="deleteSchedule()"
          variant="danger"
          class="align-middle"
        >
          <font-awesome-icon icon="calendar-minus" />
        </b-button>
      </div>
    </div>
  </b-list-group-item>
</template>

<style scoped></style>
