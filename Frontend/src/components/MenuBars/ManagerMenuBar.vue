<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title>Allinone WFH System</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="personal">My Schedule</v-btn>
    <v-btn text @click="team">My Team's Schedule</v-btn>
    <v-btn text @click="overall">Teams Under Me</v-btn>
    <v-btn text @click="logout">Logout</v-btn>
  </v-app-bar>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    wfhRequests(){
      this.$router.push({ name: '/manager/ProcessWFH' });
    },
    team(){
      this.$router.push({ name: '/manager/TeamSchedule' });
    },
    personal(){
      this.$router.push({ name: '/manager/PersonalSchedule' });
    },
    overall(){
      this.$router.push({ name: '/manager/OverallSchedule' });
    },
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push({ name: '/' });
    }
  },
};
</script>
