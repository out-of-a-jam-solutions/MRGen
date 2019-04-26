<script>
export default {
  // component setup
  name: "Schedule",

  // component data
  props: {
    schedule: {
      type: Object,
      required: true
    }
  }
};
</script>

<template>
  <b-list-group-item>
    Task Type: {{ schedule.task_type }}
    <br/>
    Run schedule: {{ schedule.periodic_task }}
  </b-list-group-item>
</template>

<style scoped></style>
