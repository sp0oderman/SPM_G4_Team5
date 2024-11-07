<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title>Allinone WFH System</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="surbordinate">My Team's Schedule</v-btn>
    <v-btn text @click="overall">All Teams</v-btn>
    <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  methods: {
    surbordinate(){
      this.$router.push({ name: '/ceo/SurbordinateSchedule' });
    },
    overall(){
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
