<template>
  <div class="legend">
    <div class="legend-item">
      <span class="color-box rejected"></span>
      <span>Rejected</span>
    </div>
    <div class="legend-item">
      <span class="color-box pending"></span>
      <span>Pending</span>
    </div>
    <div class="legend-item">
      <span class="color-box approved"></span>
      <span>Approved</span>
    </div>
  </div>
</template>

<script>
</script>

<style scoped>
.legend {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}
.legend-item {
  display: flex;
  align-items: center;
}
.color-box {
  width: 20px;
  height: 20px;
  margin-right: 0.5rem;
}
.pending {
  background-color: red;
}
.pending {
  background-color: orange;
}
.approved {
  background-color: green;
}
</style>