<template>
    <FullCalendar :options="calendarOptions" />
  
    <AlertMessage 
        v-if="alertMessage.status" 
        :key="alertMessage.key"
        :status="alertMessage.status" 
        :message="alertMessage.message"
      />
  
  </template>
    
  <script>
  import FullCalendar from '@fullcalendar/vue3';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import interactionPlugin from '@fullcalendar/interaction';
  import axios from 'axios';
  import { useAuthStore } from '@/stores/auth';
  
  export default {
    components: {
      FullCalendar
    },
    data() {
      const today = new Date();
      const startDate = new Date(today);
      startDate.setMonth(today.getMonth() - 2);
      const endDate = new Date(today);
      endDate.setMonth(today.getMonth() + 3);
      endDate.setDate(today.getDate() + 1);
      
      const getUser = useAuthStore().getUser;
      const reportingId = getUser.staff_id;
  
      return {
        user: getUser,
        reportingManagerId: reportingId,
        teamSize: 0,
        calendarOptions: {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: 'dayGridMonth',
          dateClick: this.handleDateClick,
          events: [],
          validRange: {
            start: startDate.toISOString().split('T')[0],
            end: endDate.toISOString().split('T')[0]
          }
        },
        count: 0,
        alertMessage: {
          key: 0,
          status: '',
          message: ''
        }
      };
    },
    methods: {
      async getTeamSize(){
        try {
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/team/size/${this.reportingManagerId}`);
          if (response.data.code === 200) {
            this.teamSize = response.data.data.team_size;
          } 
          else {
            this.count = this.count + 1;
            this.alertMessage = {
              key: this.count,
              status: 'fail',
              message: 'No reporting managers found.'
            };
          }
        } 
        catch (error) {
          this.count = this.count + 1;
          this.alertMessage = {
            key: this.count,
            status: 'fail',
            message: error.response.data.message
          };
          console.error('Error fetching reporting managers:', error);
        }
      },
      async loadTeamSchedule() {
        await this.getTeamSize();
  
        if (this.selectedManager === null) {
          return;
        }
  
        try {
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/strength/${this.reportingManagerId}/${this.calendarOptions.validRange.start}/${this.calendarOptions.validRange.end}`);
          const dates = response.data.data.dates;
          const events = Object.keys(dates).map(date => {
            const numOfStaff = dates[date];
            return [
              { title: `AM: ${numOfStaff.AM} / ${this.teamSize}`, date: new Date(date).toISOString().split('T')[0] },
              { title: `PM: ${numOfStaff.PM} / ${this.teamSize}`, date: new Date(date).toISOString().split('T')[0] }
            ];
          }).flat();
  
          this.calendarOptions.events = events;
  
          if (events.length === 0) {
            this.count = this.count + 1;
            this.alertMessage = {
              key: this.count,
              status: 'fail',
              message: error.response.data.message
            };
            console.error('No WFH requests.');
          }
          
        } 
        catch (error) {
          console.error('Error fetching WFH schedule:', error);
          this.count = this.count + 1;
          this.alertMessage = {
            key: this.count,
            status: 'fail',
            message: error.response.data.message
          };
        }
      },
    },
    async mounted() {
      await this.loadTeamSchedule();
    }
  };
  </script>