<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title>Allinone WFH System</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="personal">My Schedule</v-btn>
    <v-btn text @click="team">My Team's Schedule</v-btn>
    <v-btn text @click="overallSchedule">All Teams</v-btn>
    <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    overallSchedule(){
      this.$router.push({ name: '/hr/OverallSchedule' });
    },
    team(){
      this.$router.push({ name: '/hr/TeamSchedule' });
    },
    personal(){
      this.$router.push({ name: '/hr/PersonalSchedule' });
    },
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push({ name: '/' });
    }
  },
};
</script>
