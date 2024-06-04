<template>
    <Bar
      id="saving-chart"
      :options="chartOptions"
      :data="chartData"
    />
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'SavingChart',
    components: { Bar },
    props: ['savingData'],
    data() {
      return {
        chartOptions: {
          responsive: true,
          plugins: {
            Legend: {
              display: true
            }
          }
        }
      }
    },
    computed: {
      chartData() {
        return {
          labels: this.savingData.map(item => item.name),
          datasets: [{
            data: this.savingData.map(item => item.count),
            label: '가입자(명)',
            backgroundColor: '#E3EEFF',
          }]
        }
      }
    }
  }
  </script>
  