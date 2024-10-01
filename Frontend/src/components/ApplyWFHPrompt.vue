<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title class="headline">Selected WFH Date: {{ selectedDate }}</v-card-title>
      <v-card-text>
        <v-radio-group v-model="selectedOption" :mandatory="false">
          <v-radio label="AM" value="AM"></v-radio>
          <v-radio label="PM" value="PM"></v-radio>
          <v-radio label="Full Day" value="FullDay"></v-radio>
        </v-radio-group>
        <v-textarea v-model="comment" label="Comments (Optional)" outlined></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="send" :disabled="!selectedOption">Send</v-btn>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      selectedOption: null,
      comment: '',
      selectedDate: null,
    }
  },
  methods: {
    resetFields() {
      this.selectedOption = null;
      this.comment = '';
      this.selectedDate = '';
    },
    open(date) {
      this.selectedDate = date;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.resetFields();
    },
    send() {
      this.$emit('submit', { date: this.selectedDate, option: this.selectedOption, comment: this.comment });
      this.close();
    }
  }
}
</script>