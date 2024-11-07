<template>
    <div>
      <ViewWithdrawalRequests
        :requests="withdawalRequests"
        @update-requests="fetchWithdawalRequests"
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
      withdawalRequests: [],
      count:0,
      alertMessage: {
        key: 0,
        status: '',
        message: ''
      }
    };
  },
  mounted() {
    this.fetchWithdawalRequests();
  },
  methods: {
    async fetchWithdawalRequests() {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/withdrawal_requests/staff_id/${useAuthStore().getUser.staff_id}/All`);
        
        if (!response.ok) {
          throw new Error("Failed to fetch withdrawal requests");
        }
        const data = await response.json();
        
        this.withdawalRequests = data.data.requests;
      } 
      catch (error) {
        console.error("Error fetching withdrawal requests:", error);
        this.count = this.count + 1;
        this.alertMessage = {
          key: this.count,
            status: 'fail',
            message: "No Withdrawal requests"
        };
      }
    }
  }
};
</script>