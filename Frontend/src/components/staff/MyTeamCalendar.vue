<template>
  <FullCalendar :options="calendarOptions" />
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

    return {
      user: useAuthStore().getUser,
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        dateClick: this.handleDateClick,
        events: [],
        validRange: {
          start: startDate.toISOString().split('T')[0],
          end: endDate.toISOString().split('T')[0]
        }
      }
    };
  },
  methods: {
    async getTeamSize(){
      try {
        if (useAuthStore().getAccessControl === "ceo"){
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/strength/${this.user.staff_id}/${this.calendarOptions.validRange.start}/${this.calendarOptions.validRange.end}`);
        }
        else{
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/strength/${this.user.reporting_manager}/${this.calendarOptions.validRange.start}/${this.calendarOptions.validRange.end}`);
        }
      }
      catch (error) {
        console.error('Error fetching team WFH schedule:', error);
      }
    },
    async loadTeamSchedule() {
      try {
        if (useAuthStore().getAccessControl === "ceo"){
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/strength/${this.user.staff_id}/${this.calendarOptions.validRange.start}/${this.calendarOptions.validRange.end}`);
        }
        else{
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/strength/${this.user.reporting_manager}/${this.calendarOptions.validRange.start}/${this.calendarOptions.validRange.end}`);
        }
        
        
        if (response.data.code === 200) {
          const events = response.data.data.team_requests.map(request => ({
            title: `WFH: ${request.staff_id}`,
            date: new Date(request.chosen_date).toISOString().split('T')[0],
          }));

          this.calendarOptions.events = events;

          if (events.length === 0) {
          console.error('No WFH requests found for the team.');
          }
        } 
      } 
      catch (error) {
        console.error('Error fetching team WFH schedule:', error);
      }
    },
  },
  async mounted() {
    await this.loadTeamSchedule();
  }
};
</script>
