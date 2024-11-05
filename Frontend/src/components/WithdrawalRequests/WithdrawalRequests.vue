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
            <p><strong>Staff:</strong> {{ request.staff_id }}</p>
            <p><strong>Date:</strong> {{ request.request_datetime }}</p>
            <p><strong>Remarks:</strong> {{ request.remarks }}</p>
            <p><strong>Reason for Status:</strong> {{ request.reason_for_status }}</p>
            <p><strong>Status:</strong> {{ request.status }}</p>
        </v-expansion-panel-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" variant="text" @click="openDialog(request)" :disabled="request.status !== 'Pending'">
                Approve / Reject
            </v-btn>
        </v-card-actions>
        </v-expansion-panel>

        <!-- Request Dialog -->
        <v-dialog v-model="dialog" max-width="600px">
        <v-card>
            <v-card-title class="headline">Selected Withdrawal Request: {{ this.request.request_id }}</v-card-title>
            <v-card-text>
            <v-textarea v-model="reason" label="Reason for approval / rejection (Mandatory)" outlined></v-textarea>
            </v-card-text>
            <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="approveRequest" :disabled="!reason">
                Approve
            </v-btn>
            <v-btn color="blue darken-1" text @click="rejectRequest" :disabled="!reason">
                Reject
            </v-btn>
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
      reason: '',
      request: null
    };
  },
  methods: {
    async approveRequest() {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/withdrawal_requests/approve_withdrawal_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.request.request_id,
            reason_for_status: this.reason
          })
        });
        this.closeDialog();
      } 
      catch (error) {
        console.error("Error approving request:", error);
      }
    },
    async rejectRequest() {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/withdrawal_requests/reject_withdrawal_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.request.request_id,
            reason_for_status: this.reason
          })
        });
        this.closeDialog();
      } 
      catch (error) {
        console.error("Error rejecting request:", error);
      }
    },
    openDialog(request) {
      this.request = request;
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      // this.reason = '';
      // this.request = null;
    },
  }
};
</script>