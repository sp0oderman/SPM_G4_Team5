<template>
  <ManagerMenuBar/>
  <div>
    <Requests
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
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/pending_wfh_requests?manager_id=${useAuthStore().getUser.staff_id}`);
        if (!response.ok) {
          throw new Error("Failed to fetch pending requests");
        }
        const data = await response.json();
        this.pendingRequests = data;
      } catch (error) {
        console.error("Error fetching pending requests:", error);
      }
    }
  }
};
</script>
