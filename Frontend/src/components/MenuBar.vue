<template>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>SPM WFH Project</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="personal">Personal</v-btn>
      <v-btn text @click="team">Team</v-btn>
      <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>
  </template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    personal(){
      this.$router.push({ name: '/Schedule' });
    },
    team(){
      this.$router.push({ name: '/TeamSchedule' });
    },
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push({ name: '/' });
    }
  },
};
</script>
