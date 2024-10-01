import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    error: null,
  }),
  actions: {
    async authenticate(email) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/employees/auth/${email}`);
        if (response.data.code === 200) {
          this.user = response.data.data;
          this.error = null;
        } 
        else {
          this.user = null;
          this.error = response.data.message;
        }
      } 
      catch (error) {
        this.user = null;
        this.error = 'An error occurred while trying to authenticate.';
      }
    },
    logout() {
      this.user = null;
      this.error = null;
    },
  },
  getters: {
    getUser: state => state.user
  },
  persist: true,
});