// Utilities
import { defineStore } from 'pinia'
export const useUserStore = defineStore('user', {
  state: () => ({
    userId: null
  }),
  actions: {
    setUserId(userId) {
      this.userId = userId;
    }
  },
  getters: {
    getUserId: state => state.userId
  },
  persist: true,
});
