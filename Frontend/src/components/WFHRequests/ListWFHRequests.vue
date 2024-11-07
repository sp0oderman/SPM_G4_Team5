<template>
    <div>
      <WFHRequests
        :requests="pendingRequests"
        @update-requests="fetchPendingRequests"
      />
    </div>
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
    data() {
      return {
        pendingRequests: [],
        alertMessage: {
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
          const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/${useAuthStore().getUser.staff_id}/All`);
          if (!response.ok) {
            throw new Error("Failed to fetch pending requests");
          }
          const data = await response.json();
          
          this.pendingRequests = data.data.team_requests;
        } 
        catch (error) {
          console.error("Error fetching pending requests:", error);
          this.alertMessage = {
            status: 'fail',
            message: "No requests"
          };
        }
      }
    }
  };
  </script>  