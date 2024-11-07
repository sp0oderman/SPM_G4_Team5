<template>
    <div>
      <ViewWFHRequests
        :requests="pendingRequests"
        @update-requests="fetchPendingRequests"
      />
    </div>
    <AlertMessage
      v-if="alertMessage.status"
      :status="alertMessage.status"
      :message="alertMessage.message"
      :key="alertMessage.key"
    />
  </template>
  
  <script>
  import { useAuthStore } from '@/stores/auth';
  
  export default {
    data() {
      return {
        pendingRequests: [],
        count: 0,
        alertMessage: {
          key: 0,
          status: '',
          message: ''
        }
      };
    },
    mounted() {
      this.fetchPendingRequests();
    },
    methods: {
      async fetchPendingRequests() {
        try {
          const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/staff_id/${useAuthStore().getUser.staff_id}/All`);
          if (!response.ok) {
            throw new Error("Failed to fetch pending requests");
          }
          const data = await response.json();
          this.pendingRequests = data.data.requests;
        } 
        catch (error) {
          console.error("Error fetching pending requests:", error);
          this.count = this.count + 1;
          this.alertMessage = {
            key: this.count,
            status: 'fail',
            message: "No WFH requests"
          };
        }
      }
    }
  };
  </script>  