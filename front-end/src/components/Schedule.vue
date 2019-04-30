<script>
import cronstrue from 'cronstrue';

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
  methods: {
    parseCron(task) {
      const cronstring = task.minute + " " +
                         task.hour + " " +
                         task.day_of_week + " " +
                         task.day_of_month + " " +
                         task.month_of_year
      return cronstrue.toString(cronstring, { verbose: true });
    }
  }
};
</script>

<template>
  <b-list-group-item>
    Task Type: {{ schedule.task_type }}
    <br/>
    Run schedule: {{ parseCron(schedule.periodic_task) }}
  </b-list-group-item>
</template>

<style scoped></style>
