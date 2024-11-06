<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="pa-4" width="600">
      <v-card-title>
        <span class="headline">Login</span>
      </v-card-title>
      <v-card-subtitle>
        <v-form validate-on="submit lazy" @submit.prevent="submit">
          <v-text-field 
            v-model="email" 
            :rules="emailRules" 
            label="Email" 
            outlined 
            full-width>
          </v-text-field>
          <v-row class="mt-3" justify="center">
            <v-col cols="auto">
              <v-btn :loading="loading" color="primary" type="submit" block>
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
  data() {
    return {
      email: '',
      loginError: null,
      loading: false,
      emailRules: [
        value => !!value || 'Please enter an email.',
        value => this.isValidEmail(value) || 'Please enter a valid email address.'
      ],
    };
  },
  methods: {
    isValidEmail(email) {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(email);
    },
    async submit() {
      this.loading = true;
       // Reset error before submission
      this.loginError = null;
      const authStore = useAuthStore();

      // Check if email is valid before authentication
      if (!this.isValidEmail(this.email)) {
        this.loginError = 'Invalid email format.';
        this.loading = false;
        return;
      }

      await authStore.authenticate(this.email);

      if (authStore.error) {
        this.loginError = authStore.error;
        authStore.reset();
      } 
      else {
        const userRole = authStore.getUser.role;
        const userDept = authStore.getUser.dept;
        
        if (userDept === "CEO"){
          authStore.setAccessControl("ceo");
          this.$router.push({ name: '/ceo/OverallSchedule'});
        }
        else if (userDept === "HR"){
          authStore.setAccessControl("hr");
          this.$router.push({ name: '/hr/PersonalSchedule' })
        }
        else if (userRole === 2) {
          authStore.setAccessControl("staff");
          this.$router.push({ name: '/staff/PersonalSchedule' });
        } 
        else if (userRole === 1 || userRole === 3) {
          authStore.setAccessControl("manager");
          this.$router.push({ name: '/manager/PersonalSchedule' });
        }
      }

      this.loading = false;
    },
  },
};
</script>

<style scoped>
.v-container {
  max-width: 800px;
}
</style>