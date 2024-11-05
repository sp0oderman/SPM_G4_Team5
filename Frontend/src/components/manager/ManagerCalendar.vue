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
      teamSize: 0,
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
    async getTeamSize() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/team/size/${this.user.staff_id}`);
        if (response.data.code === 200) {
          this.teamSize = response.data.data.team_size;
        } 
      } 
      catch (error) {
        console.error('Error fetching team size', error);
      }
    },
    async loadTeamSchedule() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/${this.user.staff_id}`);
        
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
    await this.getTeamSize();
    await this.loadTeamSchedule();
  }
};
</script>