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
                Login
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
        if (useAuthStore().getUser.role === 1) {
          this.$router.push({ name: '/hr/OverallSchedule' });
        }
        else if (useAuthStore().getUser.role === 2) {
          this.$router.push({ name: '/staff/Schedule' });
        }

        else if (useAuthStore().getUser.role === 3) {
          this.$router.push({ name: '/manager/TeamSchedule' });
        }
      } 
      else {
        this.loginError = authStore.error;
        useAuthStore().reset();
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