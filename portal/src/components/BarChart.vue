<template>
    <div class="grid grid-cols-1 w-full">
      <div>
        <Bar
          id="BarChart"
          v-if="loaded"
          :data="chartData"
        />
      </div>
      <div class="bg-white rounded-xl border-2 pt-2 px-2 mt-4 mx-6">
        <p class="text-sm font-normal text-gray-800" v-for="item in service_institution" :key="item">
          {{ item }}
        </p>
      </div>
    </div>
</template>
  
<script>
  import { API } from '@/api'
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
  
  export default {
    name: 'BarChart',
    components: { Bar },
    data: () => ({
      loaded: false,
      chartData: null,
      service_institution: [],
    }),
    async mounted(){
      this.loaded = false;
      try {
        const response = await API.get('data/best_request_service');
        const colors = ['#41B883', '#E46651', '#00D8FF', '#ad5dd8', '#5750db', '#38af5b', '#aa5935', '#e49585', '#7bdaaa', '#000000']
        this.chartData = {
          labels: [],
          datasets: [
            {
              label: 'Servicio - Institucion: Cantidad de solicitudes',
              backgroundColor: [],
              data: []
            },
          ]
        };
        let i = 0;
        for (const prop in response.data) {
          this.chartData.labels.push("(" + i + ")");
          this.service_institution.push("(" + i + ") " + prop + " - " + response.data[prop] + " solicitudes");
          this.chartData.datasets[0].backgroundColor.push(colors[i]);
          this.chartData.datasets[0].data.push(response.data[prop]);
          i ++;
        }
        
        this.loaded = true;
      } catch (e) {
        console.error(e);
      }
    }
  }
</script>