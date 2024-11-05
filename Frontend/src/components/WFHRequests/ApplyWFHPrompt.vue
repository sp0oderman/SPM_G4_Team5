<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title class="headline">Selected WFH Date: {{ selectedDate }}</v-card-title>
      <v-card-text>
        <v-row no-gutters>
          <v-col>
            <v-radio-group v-model="selectedOption" :mandatory="false">
              <p><strong>WFH Time:</strong></p>
              <v-radio label="AM" value="AM"></v-radio>
              <v-radio label="PM" value="PM"></v-radio>
              <v-radio label="Full Day" value="Full Day"></v-radio>
            </v-radio-group>
          </v-col>

          <v-col>
            <v-radio-group v-model="selectRecurring" :mandatory="false">
              <p><strong>Repeat WFH Days:</strong></p>
              <v-radio label="Yes" value="1"></v-radio>
              <v-radio label="No" value="-1"></v-radio>
            </v-radio-group>
            <v-text-field
              v-if="selectRecurring === '1'"
              v-model="numOfWeeks"
              label="Number of Weeks"
              outlined
              type="number"
              :rules="[
                v => !v || /^[1-9]\d*$/.test(v) || 'Must be a whole number greater than 0'
              ]"
              @keypress="isWholeNumber"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-textarea
          v-model="comment"
          label="Remarks (Mandatory)"
          outlined
          :rules="[v => !!v || 'Remarks are required']"
        ></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="send" :disabled="!comment || !selectedOption || !selectRecurring">Send</v-btn>
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
      selectRecurring: null,
      numOfWeeks: null,
      comment: '',
      selectedDate: null,
      endDate: null,
    }
  },
  methods: {
    resetFields() {
      this.selectedOption = null;
      this.selectRecurring = null;
      this.recurringCount = null;
      this.comment = '';
      this.selectedDate = null;
      this.endDate = null;
    },
    open(date) {
      this.selectedDate = date;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.resetFields();
    },
    calculateEndDate(numOfWeeks) {
      const today = new Date(this.selectedDate);
      const endDate = new Date(today);
      endDate.setDate(today.getDate() + 7 * numOfWeeks);
      this.endDate = endDate.toISOString().split('T')[0];
    },
    send() {
      if (this.selectRecurring === '1'){
        this.selectRecurring = 1;
        this.calculateEndDate(this.numOfWeeks);
      }
      else{
        this.selectRecurring = -1;
        this.endDate = null;
      }
      this.$emit('submit', {
          date: this.selectedDate,
          arrangement_type: this.selectedOption,
          comment: this.comment,
          endDate: this.endDate,
          recurring_id: this.selectRecurring,
      });
      this.close();
    },
    isWholeNumber(event) {
      const char = String.fromCharCode(event.which);
      if (!/[0-9]/.test(char)) {
        event.preventDefault();
      }
    }
  }
}
</script>