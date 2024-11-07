<template>
  <v-snackbar
    v-model="snackbar"
    multi-line
    :color="snackbarColor"
    :timeout="3000"
  >
    {{ snackbarText }}
    <template v-slot:actions>
      <v-btn color="white" variant="text" @click="snackbar = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  props: {
    status: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      snackbar: false,
      snackbarText: this.message,
      snackbarColor: this.status === 'success' ? 'green-darken-2' : 'red-darken-2'
    };
  },
  watch: {
    status(newStatus) {
      this.snackbarColor = newStatus === 'success' ? 'green-darken-2' : 'red-darken-2';
    },
    message(newMessage) {
      this.snackbarText = newMessage;
    }
  },
  mounted() {
    this.snackbar = true;
  }
};
</script>