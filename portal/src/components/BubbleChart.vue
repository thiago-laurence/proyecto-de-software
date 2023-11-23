<template>
    <Bubble
            id="BubbleChart"
            v-if="loaded"
            :data="chartData"
        />
</template>
  
<script>
  import { API } from '@/api'
  import { Bubble } from 'vue-chartjs'
  import { Chart as ChartJS, PointElement, Tooltip, Legend, LinearScale } from 'chart.js'
  
  ChartJS.register(LinearScale, PointElement, Tooltip, Legend)
  
  export default {
    name: 'BubbleChart',
    components: { Bubble },
    data: () => ({
      loaded: false,
      chartData: null
    }),
    async mounted(){
      this.loaded = false;
      try {
        const response = await API.get('data/best_institutions_resolution');
        const colors = ['#41B883', '#E46651', '#00D8FF', '#ad5dd8', '#5750db', '#38af5b', '#aa5935', '#e49585', '#7bdaaa', '#000000']

        this.chartData = {
            datasets: []
        };
        let i = 1;
        for (const prop in response.data) {
            let data = {
                label: prop,
                backgroundColor: colors[i],
                data: [{
                        x: response.data[prop][0],
                        y: response.data[prop][1],
                        r: 5
                    }]
            }
            this.chartData.datasets.push(data);
            i ++;
        }
        
        this.loaded = true;
      } catch (e) {
        console.error(e);
      }
    }
  }
</script>