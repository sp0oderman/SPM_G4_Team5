<template>
    <v-btn variant="outlined" text @click="team">
        My WFH Requests
    </v-btn>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    team(){
      this.$router.push({ name: `/${useAuthStore().getAccessControl}/PersonalWFHRequests` });
    }
  },
};
</script>