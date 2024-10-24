<template>
  <FullCalendar :options="calendarOptions" />
  <ApplyWFHPrompt ref="applyWFHPrompt" @submit="handleSubmit" />
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth';

export default {
  components: {
    FullCalendar
  },
  data() {
    // Calculate date ranges based on customer requirement
    // -2 months from today
    // +3 months from today
    const today = new Date();
    const startDate = new Date(today);
    startDate.setMonth(today.getMonth() - 2);
    const endDate = new Date(today);
    endDate.setMonth(today.getMonth() + 3);
    endDate.setDate(today.getDate() + 1);

    return {
      calendarOptions: {
        plugins: [ dayGridPlugin, interactionPlugin ],
        initialView: 'dayGridMonth',
        dateClick: this.handleDateClick,
        // TODO: List out personal calendar with existing WFH applications
        events: [
          { title: 'Test event', date: '2024-10-01' },
        ],
        validRange: {
          start: startDate.toISOString().split('T')[0],
          end: endDate.toISOString().split('T')[0]
        }
      }
    }
  },
  methods: {
    handleDateClick(arg) {
      this.$refs.applyWFHPrompt.open(arg.dateStr);
    },

    async handleSubmit(data) {
      console.log('Selected date:', data.date);
      console.log('Selected option:', data.option);
      console.log('Comment:', data.comment);
      console.log('id:', useAuthStore().getUser.staff_id);

      const payload = {
        staff_id: useAuthStore().getUser.staff_id,
        requested_dates: [data.date],
        time_of_day: data.option,
        reason: data.comment
      };

      try {
        //Modify link accordingly
        const response = await axios.post('http://127.0.0.1:5000/wfh_requests/apply_wfh', payload);
        if (response.status === 200) {
          console.log("successfully applied")
        } 
        else {
          console.log("failed to apply")
        }
      } 
      catch (error) {
        console.log("failed to apply")
      }
    },
    
    async loadSchedule() {
      try {
        const user = useAuthStore().getUser;
        const response = await axios.get(`/wfh_requests/staff_id/${user.staff_id}`);
        
        if (response.data.code === 200) {
          const events = response.data.data.team_requests.map(request => ({
            title: `WFH`,
            date: request.chosen_date,
          }));

          this.calendarOptions.events = events;
        } else {
          console.error('No WFH requests found for the user.');
        }
      } catch (error) {
        console.error('Error fetching WFH schedule:', error);
      }
    },
  },
  async mounted() {
    await this.loadSchedule();
  }
}
</script>
