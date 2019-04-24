<template>
  <div>
    <h1>{{customer.name}}</h1>
  </div>
</template>

<script>
export default {
  name: "Customer",
  props: [
    "customer"
  ]
};
</script>

<style scoped></style>
