<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title class="headline">Withdraw WFH: {{ selectedDate }}</v-card-title>
      <v-card-text>
        <v-textarea v-model="reason" label="Reason for withdrawal (Mandatory)" outlined></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="withdraw">Confirm</v-btn>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <!-- AlertMessage -->
  <AlertMessage
      v-if="alertMessage.status"
      :status="alertMessage.status"
      :message="alertMessage.message"
      :key="alertMessage.message"
    />
</template>
  
<script>
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  emits: ['wfh-withdrawn'],
  data() {
    return {
      dialog: false,
      selectedDate: null,
      requestId: null,
      reason: "",
      alertMessage: {
        status: '',
        message: ''
      }
    };
  },
  methods: {
    open({ date, requestId }) {
      this.reason = "";
      this.selectedDate = date;
      this.requestId = requestId;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
    async withdraw() {
      try {
        const user = useAuthStore().getUser;
        const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/withdrawal_requests/apply_withdrawal_request`, {
          staff_id: user.staff_id,
          reporting_manager: user.reporting_manager,
          wfh_request_id: this.requestId,
          remarks: this.reason,
          request_datetime: new Date().toISOString()
        });
        this.alertMessage = {
          status: 'Success',
          message: 'Request approved successfully!'
        };
        this.$emit('wfh-withdrawn');
        this.close();
      } 
      catch (error) {
        console.log('Failed to withdraw', error);
        this.alertMessage = {
          status: 'fail',
          message: "Failed to withdraw"
        };
      }
    },
  },
};
</script>