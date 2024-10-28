<template>
  <v-expansion-panels>
    <v-expansion-panel
      v-for="request in requests"
      :key="request.id"
    >
      <v-expansion-panel-title>
        Request from {{ request.staff_id }}
      </v-expansion-panel-title>
      
      <v-expansion-panel-text>
        <p><strong>Requested Date:</strong> {{ request.requested_dates }}</p>
        <p><strong>Time of Day:</strong> {{ request.time_of_day }}</p>
        <p><strong>Reason:</strong> {{ request.reason }}</p>
        <p><strong>Status:</strong> {{ request.status }}</p>
      </v-expansion-panel-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="secondary"
          variant="text"
          @click="openRejectDialog(request.id)"
        >
          Reject
        </v-btn>
        <v-btn
          color="primary"
          variant="text"
          @click="acceptRequest(request.id)"
        >
          Accept
        </v-btn>
      </v-card-actions>
    </v-expansion-panel>

    <!-- Reject Request Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">Reject request no: {{ selectedRequestId }}</v-card-title>
        <v-card-text>
          <v-textarea v-model="rejectionReason" label="Reason for rejection" outlined></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="confirmReject" :disabled="!rejectionReason">
            Confirm
          </v-btn>
          <v-btn color="blue darken-1" text @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-expansion-panels>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  props: {
    requests: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      dialog: false,
      rejectionReason: '',
      selectedRequestId: null
    };
  },
  methods: {
    async acceptRequest(requestId) {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/approve_wfh_request`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: requestId, 
            manager_id: useAuthStore().getUser.staff_id,
          })
        });
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error approving request:", error);
      }
    },
    openRejectDialog(requestId) {
      this.selectedRequestId = requestId;
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      this.rejectionReason = '';
      this.selectedRequestId = null;
    },
    async confirmReject() {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/reject_wfh_request`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.selectedRequestId, 
            rejection_reason: this.rejectionReason 
          })
        });
        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error rejecting request:", error);
      }
    }
  }
};
</script>