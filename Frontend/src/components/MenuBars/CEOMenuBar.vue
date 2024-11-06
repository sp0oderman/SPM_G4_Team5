<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title>Allinone WFH System</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="teamSchedule">My Team's Schedule</v-btn>
    <v-btn text @click="overallSchedule">All Teams</v-btn>
    <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    teamSchedule(){
      this.$router.push({ name: '/ceo/TeamSchedule' });
    },
    overallSchedule(){
      this.$router.push({ name: '/ceo/OverallSchedule' });
    },
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push({ name: '/' });
    }
  },
};
</script>
