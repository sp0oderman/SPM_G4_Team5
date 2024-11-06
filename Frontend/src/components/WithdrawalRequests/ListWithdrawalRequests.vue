<template>
    <div>
      <WithdrawalRequests
        :requests="withdawalRequests"
        @update-requests="fetchWithdawalRequests"
      />
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  data() {
    return {
      withdawalRequests: []
    };
  },
  mounted() {
    this.fetchWithdawalRequests();
  },
  methods: {
    async fetchWithdawalRequests() {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/withdrawal_requests/team/${useAuthStore().getUser.staff_id}/All`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch withdrawal requests");
        }
        const data = await response.json();
        console.log(data.data.team_requests)
        this.withdawalRequests = data.data.team_requests;
      } 
      catch (error) {
        console.error("Error fetching withdrawal requests:", error);
      }
    }
  }
};
</script>