<template>
  <FullCalendar :options="calendarOptions" />
  <ApplyWFHPrompt ref="applyWFHPrompt" @submit="handleApply" />
  <WithdrawWFHDialog ref="withdrawWFHDialog" @wfh-withdrawn="loadSchedule" />
</template>

<script>
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  components: {
    FullCalendar,
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
        eventClick: this.handleEventClick,
        events: [],
        validRange: {
          start: startDate.toISOString().split('T')[0],
          end: endDate.toISOString().split('T')[0],
        },
      },
    };
  },
  methods: {
    handleDateClick(arg) {
      this.$refs.applyWFHPrompt.open(arg.dateStr);
    },

    handleEventClick(info) {
      const eventObj = info.event;
      if (eventObj.extendedProps.requestId) {
        // Open the withdraw dialog with the request date and ID
        this.$refs.withdrawWFHDialog.open({
          date: eventObj.start.toISOString().split('T')[0],
          requestId: eventObj.extendedProps.requestId,
        });
      } else {
        alert('Event cannot be withdrawn.');
      }
    },

    async handleApply(data) {
      const user = useAuthStore().getUser;
      const payload = {
        staff_id: user.staff_id,
        reporting_manager: user.reporting_manager,
        dept: user.dept,
        chosen_date: data.date,
        arrangement_type: data.option,
        request_datetime: new Date().toISOString(),
        status: 'Pending',
        remarks: data.comment,
      };

      try {
        const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/apply_wfh`, payload);
        console.log(response.status === 200 ? 'successfully applied' : 'failed to apply');
      } 
      catch (error) {
        console.log('failed to apply');
      }
    },

    async loadSchedule() {
      try {
        const user = useAuthStore().getUser;
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/staff_id/${user.staff_id}`);
        if (response.data.code === 200) {
          const events = response.data.data.requests.map(request => {
            let backgroundColor = '';
            if (request.status === 'Pending') {
              backgroundColor = 'orange';
            } 
            else if (request.status === 'Approved') {
              backgroundColor = 'green';
            }

            return {
              title: `${request.arrangement_type}`,
              date: new Date(request.chosen_date).toISOString().split('T')[0],
              backgroundColor,
              extendedProps: { requestId: request.request_id },
            };
          });

          this.calendarOptions.events = events;
        } 
        else {
          console.error('No WFH requests found for the user.');
        }
      } 
      catch (error) {
        console.error('Error fetching WFH schedule:', error);
      }
    },
  },
  async mounted() {
    await this.loadSchedule();
  },
};
</script>