<template>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">Withdraw WFH: {{ selectedDate }}</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="send">Confirm</v-btn>
          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        dialog: false,
        selectedDate: null,
        requestId: null,
      };
    },
    methods: {
        open({ date, requestId }) {
            this.selectedDate = date;
            this.requestId = requestId;
            this.dialog = true;
        },
        close() {
            this.dialog = false;
            this.selectedDate = null;
            this.requestId = null;
        },
        async send() {
          try {
            const response = await axios.delete(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/withdraw/request_id/${this.requestId}`);
            if (response.status === 200) {
              console.log('Successfully withdrawn');
              this.$emit('wfh-withdrawn');
            } 
            else {
              console.log('Failed to withdraw');
            }
            this.close();
          } 
          catch (error) {
            console.log('Failed to withdraw', error);
          }
        },
    },  
  };
  </script>
  