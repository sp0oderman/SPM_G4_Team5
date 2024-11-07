<template>
    <v-btn variant="outlined" text @click="team">
      Surbordinate's WFH Requests
    </v-btn>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    team(){
      this.$router.push({ name: `/${useAuthStore().getAccessControl}/TeamWFHRequests` });
    }
  },
};
</script>