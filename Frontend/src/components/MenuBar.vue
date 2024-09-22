<template>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>WFH Manager</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="navigate('home')">Home</v-btn>
      <v-btn text @click="navigate('about')">About</v-btn>
      <v-btn text @click="navigate('contact')">Contact</v-btn>
    </v-app-bar>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const navigate = (route) => {
    router.push({ name: route });
  };
  </script>
