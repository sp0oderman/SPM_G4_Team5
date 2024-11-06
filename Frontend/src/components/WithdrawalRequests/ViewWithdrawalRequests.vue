<template>
    <v-expansion-panels>
        <v-expansion-panel
        v-for="request in requests"
        :key="request.id"
        >
        <v-expansion-panel-title>
            Withdrawal Request: {{ request.request_id }}
        </v-expansion-panel-title>

        <v-expansion-panel-text>
            <p><strong>Date:</strong> {{ request.request_datetime }}</p>
            <p><strong>Remarks:</strong> {{ request.remarks }}</p>
            <p><strong>Reason for Withdrawal:</strong> {{ request.reason_for_status }}</p>
            <p><strong>Status:</strong> {{ request.status }}</p>
        </v-expansion-panel-text>
        </v-expansion-panel>

    </v-expansion-panels>
</template>
  
<script>

export default {
  props: {
    requests: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
    };
  },
  methods: {
  }
};
</script>