<template>
    <v-btn variant="outlined" text @click="team">
        My Team's Schedule
    </v-btn>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    team(){
      this.$router.push({ name: `/${useAuthStore().getAccessControl}/TeamSchedule` });
    }
  },
};
</script>