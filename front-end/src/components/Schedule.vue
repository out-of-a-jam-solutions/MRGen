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
    {{ schedule }}
  </b-list-group-item>
</template>

<style scoped></style>
