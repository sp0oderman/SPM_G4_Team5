<template>
    <div>
      <ViewWFHRequests
        :requests="pendingRequests"
        @update-requests="fetchPendingRequests"
      />
    </div>
  </template>
  
  <script>
  import { useAuthStore } from '@/stores/auth';
  
  export default {
    data() {
      return {
        pendingRequests: []
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
          console.log(data.data)
          this.pendingRequests = data.data.requests;
        } 
        catch (error) {
          console.error("Error fetching pending requests:", error);
        }
      }
    }
  };
  </script>  