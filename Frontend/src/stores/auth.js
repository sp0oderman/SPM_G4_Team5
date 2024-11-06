import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessControl: null,
    error: null,
  }),
  actions: {
    async authenticate(email) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/staff/email/${email}`);
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
        this.error = 'Invalid email';
      }
    },
    setAccessControl(role) {
      this.accessControl = role;
    },
    reset(){
      this.user = null;
      this.accessControl = null;
      this.error = null;
    },
    logout() {
      this.reset()
    },
  },
  getters: {
    getUser: state => state.user,
    getAccessControl: state => state.accessControl
  },
  persist: true,
});