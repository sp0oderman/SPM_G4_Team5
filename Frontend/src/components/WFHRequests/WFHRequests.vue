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
        <p><strong>Requested Date:</strong> {{ formatDate(request.chosen_date)}}</p>
        <p><strong>Time of Day:</strong> {{ request.arrangement_type }}</p>
        <p><strong>Remarks:</strong> {{ request.remarks }}</p>
        <p><strong>Reason for Status:</strong> {{ request.reason_for_status }}</p>
        <p><strong>Status:</strong> {{ request.status }}</p>
      </v-expansion-panel-text>
      
      <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" variant="text" @click="openDialog(request.request_id, request.recurring_id)" :disabled="request.status !== 'Pending'">
                Approve / Reject / Withdraw
            </v-btn>
        </v-card-actions>
    </v-expansion-panel>

    <!-- Request Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
        <v-card>
            <v-card-title class="headline">Selected Withdrawal Request: {{ selectedRequestId }}</v-card-title>
            <v-card-text>
            <v-textarea v-model="reason" label="Reason for Approval / Rejection / Withdrawal (Mandatory)" outlined></v-textarea>
            </v-card-text>
            <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="approveRequest" :disabled="!reason">
                Approve
            </v-btn>
            <v-btn color="blue darken-1" text @click="withdrawRequest" :disabled="!reason">
                Withdraw
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
      recurring_id: null,
      selectedRequestId: null,
    };
  },
  methods: {
    async approveRequest() {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/approve_wfh_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.selectedRequestId, 
            reporting_manager: useAuthStore().getUser.staff_id,
            reason_for_status: this.reason,
            recurring_id: this.recurring_id,
          })
        });
        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error approving request:", error);
      }
    },
    async rejectRequest(recurring_id) {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/reject_wfh_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.selectedRequestId, 
            reporting_manager: useAuthStore().getUser.staff_id,
            reason_for_status: this.reason,
            recurring_id: this.recurring_id,
          })
        });
        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error rejecting request:", error);
      }
    },
    async withdrawRequest(recurring_id) {
      try {
        await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/withdraw_wfh_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.selectedRequestId, 
            reporting_manager: useAuthStore().getUser.staff_id,
            reason_for_status: this.reason,
            recurring_id: this.recurring_id,
          })
        });
        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error rejecting request:", error);
      }
    },
    openDialog(requestId, recurring_id) {
      this.selectedRequestId = requestId;
      this.recurring_id = recurring_id;
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      this.reason = '';
      this.recurring_id = null;
      this.selectedRequestId = null;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toDateString();
    },
  }
};
</script>