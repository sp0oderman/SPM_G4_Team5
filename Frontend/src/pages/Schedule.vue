<template>
    <MenuBar/>
    <Calendar/>
</template>
  
<script>
import { useAuthStore } from '@/stores/auth';

export default {
  setup() {
    console.log('User Details:', useAuthStore().getUser.email);
  },
};
</script>