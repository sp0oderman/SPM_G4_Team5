<template>
    <v-row class="fill-height">
      <v-col>
        <v-sheet height="600">
          <v-calendar
            ref="calendar"
            :events="events"
            color="primary"
            type="month"
          ></v-calendar>
        </v-sheet>
      </v-col>
    </v-row>
  </template>
  
  <script>
    export default {
      data: () => ({
        focus: '',
        events: [],
        colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1',],
      }),
      mounted() {},
      methods: {},
    }
  </script>
  