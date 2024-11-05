<template>
  <v-select
      label="Reporting Manager"
      :items="reportingManagers"
      item-title="name"
      item-value="id"
      v-model="selectedManager"
    ></v-select>
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
      reportingManagers: [],
      teamSize: 0,
      selectedManager: null,
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
    async loadReportingManagers() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/reporting_managers_list`);
        if (response.data.code === 200) {
          this.reportingManagers = response.data.data.reporting_managers.map(manager => ({
            id: manager.staff_id,
            name: manager.staff_fname + " " + manager.staff_lname,
          }));
        } 
        else {
          console.warn('No reporting managers found.');
        }
      } 
      catch (error) {
        console.error('Error fetching reporting managers:', error);
      }
    },
    async getTeamSize(){
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/team/size/${this.selectedManager}`);
        if (response.data.code === 200) {
          this.teamSize = response.data.data.team_size;
        } 
        else {
          console.warn('No reporting managers found.');
        }
      } 
      catch (error) {
        console.error('Error fetching reporting managers:', error);
      }
    },
    async loadSpecificTeamSchedule() {
      await this.getTeamSize();

      if (this.selectedManager === null) {
        return;
      }

      try {
        const user = useAuthStore().getUser;
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/wfh_requests/team/strength/${this.selectedManager}/${this.calendarOptions.validRange.start}/${this.calendarOptions.validRange.end}`);
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
            console.error('No WFH requests.');
        }
        
      } 
      catch (error) {
        console.error('Error fetching WFH schedule:', error);
      }
    },
  },
  watch: {
    selectedManager(newVal) {
      console.log('Selected Manager:', newVal);
      this.loadSpecificTeamSchedule();
    },
  },
  async mounted() {
    await this.loadReportingManagers();
  }
};
</script>