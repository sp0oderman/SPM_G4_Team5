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
        <v-btn
          color="secondary"
          variant="text"
          @click="openDialog(request)"
          :disabled="request.status !== 'Pending'"
        >
          Approve / Reject / Withdraw
        </v-btn>
      </v-card-actions>
    </v-expansion-panel>

    <!-- Request Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">
          Selected WFH Request: {{ request.request_id }}
          <p>WFH Date: {{ formatDate(request.chosen_date) }}</p>
        </v-card-title>
        <v-card-text>
          <v-textarea
            v-model="reason"
            label="Reason for Approval / Rejection / Withdrawal (Mandatory)"
            outlined
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="approveRequest"
            :disabled="!reason"
          >
            Approve
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="withdrawRequest"
            :disabled="!reason"
          >
            Withdraw
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="rejectRequest"
            :disabled="!reason"
          >
            Reject
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-expansion-panels>

  <!-- AlertMessage -->
  <AlertMessage
      v-if="alertMessage.status"
      :status="alertMessage.status"
      :message="alertMessage.message"
      :key="alertMessage.message"
    />
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
  emits: ['update-requests'],
  data() {
    return {
      dialog: false,
      reason: '',
      request: null,
      alertMessage: {
        status: '',
        message: ''
      }
    };
  },
  methods: {
    async approveRequest() {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/approve_wfh_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.request.request_id, 
            reporting_manager: useAuthStore().getUser.staff_id,
            reason_for_status: this.reason,
            recurring_id: this.request.recurring_id,
          })
        });

        this.alertMessage = {
          status: 'success',
          message: 'Request approved successfully!'
        };
        
        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error approving request:", error);
        this.alertMessage = {
          status: 'fail',
          message: error.response.data.message
        };
      }
    },

    async rejectRequest() {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/reject_wfh_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.request.request_id, 
            reporting_manager: useAuthStore().getUser.staff_id,
            reason_for_status: this.reason,
            recurring_id: this.request.recurring_id,
          })
        });
        
        this.alertMessage = {
          status: 'success',
          message: 'Request rejected successfully!'
        }

        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error rejecting request:", error);
        this.alertMessage = {
          status: 'fail',
          message: error.response.data.message
        };
      }
    },

    async withdrawRequest() {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/withdraw_wfh_request`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ 
            request_id: this.request.request_id, 
            reporting_manager: useAuthStore().getUser.staff_id,
            reason_for_status: this.reason,
            recurring_id: this.request.recurring_id,
          })
        });

        this.alertMessage = {
          status: 'success',
          message: 'Request withdrawn successfully!'
        };

        this.closeDialog();
        this.$emit("update-requests");
      } 
      catch (error) {
        console.error("Error withdrawing request:", error);
        this.alertMessage = {
          status: 'fail',
          message: error.response.data.message
        };
      }
    },
    openDialog(request) {
      this.resetDialog();
      this.request = request;
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    resetDialog() {
      this.request = null;
      this.reason = "";
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toDateString();
    },
  }
};
</script>