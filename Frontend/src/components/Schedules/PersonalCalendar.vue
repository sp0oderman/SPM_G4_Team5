<template>
  <FullCalendar :options="calendarOptions" />
  <ApplyWFHPrompt ref="applyWFHPrompt" @submit="handleApply" />
  <WithdrawWFHDialog ref="withdrawWFHDialog" @wfh-withdrawn="loadSchedule" />
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
      count: 0,
      alertMessage: {
        key: 0,
        status: '',
        message: ''
      }
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
      } 
      else {
        this.count = this.count + 1;
        this.alertMessage = {
          key: this.count,
          status: 'fail',
          message: 'Event cannot be withdrawn.'
        };
      }
    },

    async handleApply(data) {
      const user = useAuthStore().getUser;

      const payload = {
        staff_id: user.staff_id,
        reporting_manager: user.reporting_manager,
        dept: user.dept,
        chosen_date: data.date,
        arrangement_type: data.arrangement_type,
        request_datetime: new Date().toISOString().split('T')[0],
        remarks: data.comment,
        recurring_id: data.recurring_id,
        end_date: data.endDate,
      };
      console.log(payload);

      try {
        const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/apply_wfh_request`, payload);
        this.count = this.count + 1;
        this.alertMessage = {
          key: this.count,
          status: 'successs',
          message: 'Successfully applied'
        };
      } 
      catch (error) {
        this.count = this.count + 1;
        this.alertMessage = {
          key: this.count,
          status: 'fail',
          message: 'Failed to apply'
        };
        console.log('failed to apply');
      }
    },

    async loadSchedule() {
      try {
        const user = useAuthStore().getUser;
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/staff_id/${user.staff_id}/All`);
        if (response.data.code === 200) {
          const events = response.data.data.requests.filter(request => request.status !== "Withdrawn")
          .map(request => {
            let backgroundColor = '';
            switch (request.status) {
              case 'Pending':
                backgroundColor = 'orange';
                break;
              case 'Approved':
                backgroundColor = 'green';
                break;
              case 'Rejected':
                backgroundColor = 'red';
                break;
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
          this.count = this.count + 1;
          this.alertMessage = {
            key: this.count,
            status: 'fail',
            message: 'No WFH requests found for the user.'
          };
          console.error('No WFH requests found for the user.');
        }
      } 
      catch (error) {
        this.count = this.count + 1;
        this.alertMessage = {
          key: this.count,
          status: 'fail',
          message: error.response.data.message
        };
        console.error('Error fetching WFH schedule:', error);
      }
    },
  },
  async mounted() {
    await this.loadSchedule();
  },
};
</script>