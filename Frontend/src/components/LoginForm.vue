<template>
    <v-container class="d-flex align-center justify-center fill-height">
      <v-card class="pa-4" width="600">
        <v-card-title>
          <span class="headline">Login</span>
        </v-card-title>
        <v-card-subtitle>
          <v-form v-model="valid">
            <v-text-field
              v-model="email"
              label="Email"
              :error-messages="emailErrors"
              @blur="validateEmail"
              outlined
              full-width
            ></v-text-field>
            <v-alert v-if="valid === false" type="error" class="mt-3">
              Invalid email
            </v-alert>
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
  export default {
    data() {
      return {
        email: '',
        valid: false,
        emailErrors: [],
      };
    },
    methods: {
      validateEmail() {
        // Example email validation logic
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        this.emailErrors = [];
        if (!emailPattern.test(this.email)) {
          this.valid = false;
          this.emailErrors.push('Invalid email address.');
        } else {
          this.valid = true;
        }
      },
      login() {
        this.$router.push({ name: '/Schedule' });
        
      },
    },
  };
  </script>
  
  <style scoped>
  .v-container {
    max-width: 800px;
  }
  </style>
  