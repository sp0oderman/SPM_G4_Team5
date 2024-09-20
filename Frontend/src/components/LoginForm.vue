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
  
<!-- Sample Login Logic -->
  <!-- <script>
  import { validationMixin } from "vuelidate";
  import { required } from "vuelidate/lib/validators";
  
  import { useUserStore } from "@/store/user";
  import { mapActions } from 'pinia'
  import { mapState } from 'pinia'
  
  //const store = useUserStore()
  const loginUrl = "https://personal-swk23gov.outsystemscloud.com/User_API/rest/v1/user/login/";
  
  export default {
    mixins: [validationMixin],
    data() {
      return {
          email: "",
          password: "",
          valid: null,
      };
    },
    validations: {
      email: {
        required,
      },
      password: {
        required,
      },
    },
    computed:{
      ...mapState(useUserStore, ['getUserId']),
    },
    methods: {
      ...mapActions(useUserStore, ['setUserId']),
      login(){
        console.log("Before login userId: " + this.getUserId);
        const loginDetails = {
            email: this.email,
            password: this.password
        }
        fetch(loginUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginDetails),
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response error');
            }
            return response.json();
        })
        .then(data => {
            if(data.Result.success){
                this.valid = true;
                // this.usedId = data.AuctionUser.userId;
                console.log(data.AuctionUser.userId);
                this.setUserId(data.AuctionUser.userId);
                console.log("getUserId is " + this.getUserId);
                this.$router.push({ name: 'Listings' });
            }
            else{
                console.log("Wrong email / password");
                console.log("getUserId is " + this.getUserId);
                this.valid = false;
            }
        })
        .catch(error => {
            console.error('Error logging in:', error);
        });
      },
      getValidationClass(fieldName) {
        const field = this.$v[fieldName];
        if (field) {
          return {
            "md-invalid": field.$invalid && field.$dirty,
          };
        }
      },
    },
  };
  </script> -->