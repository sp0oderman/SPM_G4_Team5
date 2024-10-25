<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="pa-4" width="600">
      <v-card-title>
        <span class="headline">Login</span>
      </v-card-title>
      <v-card-subtitle>
        <v-form>
          <v-text-field v-model="email" label="Email" outlined full-width></v-text-field>
          <v-row class="mt-3" justify="center">
            <v-col cols="auto">
              <v-btn color="primary" @click="login">
                WFH System Login
              </v-btn>
            </v-col>
          </v-row>
          <v-alert v-if="loginError" type="error" dismissible class="mt-3">
            {{ loginError }}
          </v-alert>
        </v-form>
      </v-card-subtitle>
    </v-card>
  </v-container>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  //REMOVE LATER
  setup(){
    console.log('User Details:', useAuthStore().getUser);
  },
  data() {
    return {
      email: '',
      loginError: null,
    };
  },
  methods: {
    async login() {
      const authStore = useAuthStore();
      await authStore.authenticate(this.email);
      if (authStore.user) {
        this.$router.push({ name: '/Schedule' });
      } 
      else {
        this.loginError = authStore.error;
      }
    }
  },
};
</script>

<style scoped>
.v-container {
  max-width: 800px;
}
</style>