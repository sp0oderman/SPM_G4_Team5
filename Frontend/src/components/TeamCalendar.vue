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
    async loadTeamSchedule() {
      try {
        const user = useAuthStore().getUser;
        const response = await axios.get(`http://127.0.0.1:5000/wfh_requests/team/${user.reporting_manager}`);
        
        if (response.data.code === 200) {
          const events = response.data.data.team_requests.map(request => ({
            title: `WFH: ${request.staff_fname}`,
            date: request.chosen_date,
          }));

          this.calendarOptions.events = events;
        } else {
          console.error('No WFH requests found for the team.');
        }
      } catch (error) {
        console.error('Error fetching team WFH schedule:', error);
      }
    },
  },
  async mounted() {
    await this.loadTeamSchedule();
  }
};
</script>
