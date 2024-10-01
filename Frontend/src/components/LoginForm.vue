<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="pa-4" width="600">
      <v-card-title>
        <span class="headline">Login</span>
      </v-card-title>
      <v-card-subtitle>
        <v-form>
          <v-text-field
            v-model="email"
            label="Email"
            outlined
            full-width
          ></v-text-field>
          <v-row class="mt-3" justify="center">
            <v-col cols="auto">
              <v-btn
                color="primary"
                @click="login"
              >
                Login
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-subtitle>
    </v-card>
  </v-container>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  setup(){
    console.log('User Details:', useAuthStore().getUser);
  },
  data() {
    return {
      email: '',
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
        this.emailErrors.push(authStore.error || 'Authentication failed.');
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
