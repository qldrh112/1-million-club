<template>
  <div class="chart-container">
    <canvas ref="chartContainer"></canvas>
  </div>
</template>

<script>
import { ArcElement, Chart } from 'chart.js';
import { onMounted, ref, nextTick } from 'vue';

Chart.register(ArcElement)

export default {
  props: {
    investAggresive: {
      type: Number,
      required: true
    },
    investConservative: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const chartContainer = ref(null);
    const chart = ref(null);

    onMounted(() => {
      nextTick(() => {
        const ctx = chartContainer.value.getContext('2d');
        chart.value = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['위험 선호', '안정 선호'],
            datasets: [{
              data: [props.investAggresive, props.investConservative],
              backgroundColor: ['red', 'blue']
            }]
          },
          options: {
            responsive: true
          }
        });
      });
    });

    return {
      chartContainer
    };
  }
};
</script>
