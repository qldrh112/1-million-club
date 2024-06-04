<template>
    <Bar
      id="deposit-chart"
      :options="chartOptions"
      :data="chartData"
    />
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'DepositChart',
    components: { Bar },
    props: ['depositData'],
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
          labels: this.depositData.map(item => item.name),
          datasets: [{
            data: this.depositData.map(item => item.count),
            label: '가입자(명)',
            backgroundColor: '#A4C8FF',
          }]
        }
      }
    }
  }
  </script>
  