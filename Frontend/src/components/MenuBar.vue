<template>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>WFH Manager</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text>Home</v-btn>
      <v-btn text>About</v-btn>
      <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>
  </template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push({ name: '/' });
    }
  },
};
</script>
