<template>
  <v-select
      label="Reporting Manager"
      :items="reportingManagers"
      item-title="name"
      item-value="id"
      v-model="selectedManager"
      v-show="visible"
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
      visible: false,
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
        let response = "";
        if (useAuthStore().getAccessControl === "ceo" || useAuthStore().getAccessControl === "hr"){
          response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/reporting_managers_list`);
        }
        else{
          response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/reporting_managers_under_me_list/`);
        }
        if (response.data.code === 200) {
          this.visible = true;
          this.reportingManagers = response.data.data.reporting_managers.map(manager => ({
            id: manager.staff_id,
            name: manager.staff_fname + " " + manager.staff_lname,
          }));
        }
      } 
      catch (error) {
        if (error.response && error.response.status === 404) {
          console.error('No reporting managers found.');
        } 
        else {
          console.error('Error fetching reporting managers:', error);
        }
      }
    },
    async getTeamSize(){
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/employees/team/size/${this.selectedManager}`);
        if (response.data.code === 200) {
          this.teamSize = response.data.data.team_size;
        }
      } 
      catch (error) {
        if (error.response && error.response.status === 404) {
          console.error('No team found for selected reporting manager.');
        } 
        else {
          console.error('Error fetching selected reporting manager team:', error);
        }
      }
    },
    async loadSpecificTeamSchedule() {
      await this.getTeamSize();

      if (this.selectedManager === null) {
        return;
      }

      try {
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
        
      } 
      catch (error) {
        if (error.response && error.response.status === 404) {
          console.error('No WFH requests.');
        } 
        else {
          console.error('Error fetching WFH schedule:', error);
        }
      }
    },
  },
  watch: {
    selectedManager(newVal) {
      this.loadSpecificTeamSchedule();
    },
  },
  async mounted() {
    await this.loadReportingManagers();
    if (this.reportingManagers.length === 0){
      this.selectedManager = useAuthStore().getUser.staff_id;
    }
  }
};
</script>