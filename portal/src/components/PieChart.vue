<template>
  <Pie
      id="PieChart"
      v-if="loaded"
      :data="chartData"
    />
</template>

<script>
  import { API } from '@/api'
  import { Pie } from 'vue-chartjs'
  import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'PieChart',
    components: { Pie },
    data: () => ({
      loaded: false,
      chartData: null
    }),
    async mounted(){
      this.loaded = false;
      try {
        const response = await API.get('data/cant_request');
        const colors = ['#41B883', '#E46651', '#00D8FF', '#ad5dd8', '#5750db', '#38af5b', '#aa5935', '#e49585', '#7bdaaa', '#000000']

        this.chartData = {
          labels: [],
          datasets: [
            {
              backgroundColor: [],
              data: []
            }
          ]
        };
        let i = 0;
        for (const prop in response.data) {
          this.chartData.labels.push(prop);
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