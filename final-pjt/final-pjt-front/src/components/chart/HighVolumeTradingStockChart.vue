<template>
    <Bar
      id="stock-chart"
      :options="chartOptions"
      :data="chartData"
    />
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'StockChart',
    components: { Bar },
    props: ['stockData'],
    data() {
      return {
        chartOptions: {
          responsive: true
        }
      }
    },
    computed: {
      chartData() {
        return {
          labels: this.stockData.map(item => item.name),
          datasets: [{
            data: this.stockData.map(item => item.count),
            label: '전일 대비 상승(%)',
            backgroundColor: '#E6FF89',
          }]
        }
      }
    }
  }
  </script>
  