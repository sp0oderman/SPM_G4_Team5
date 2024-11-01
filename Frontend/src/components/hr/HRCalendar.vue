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
          const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/Approved`);
          console.log(response.data.data);
          if (response.data.code === 200) {
            const events = response.data.data.wfh_requests.map(request => ({
              title: `${request.staff_id}, ${request.arrangement_type}`,
              date: new Date(request.chosen_date).toISOString().split('T')[0],
            }));
  
            this.calendarOptions.events = events;
  
            if (events.length === 0) {
                console.error('No WFH requests.');
            }
          } 
        } 
        catch (error) {
          console.error('Error fetching WFH schedule:', error);
        }
      },
    },
    async mounted() {
      await this.loadTeamSchedule();
    }
  };
  </script>
  