<template>
    <v-btn variant="outlined" text @click="team">
        Surbordinate's Schedules
    </v-btn>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    team(){
      this.$router.push({ name: `/${useAuthStore().getAccessControl}/SurbordinateSchedule` });
    }
  },
};
</script>