<template>
  <div v-if="loading" class="loading">
    <p>Loading...</p>
  </div>
  <div v-else class="stock-main">
    <h2 class="section-title">가장 많은 사람들이 가입했어요</h2>
    <div class="chart-section">
      <div class="chart-card">
        <h3 class="chart-title">예금</h3>
        <PopularDepositChart :depositData="topThree.deposit"/>
      </div>
      <div class="chart-card">
        <h3 class="chart-title">적금</h3>
        <PopularSavingChart :savingData="topThree.saving" />
      </div>
      <div class="chart-card">
        <h3 class="chart-title">주식</h3>
        <PopularStockChart :stockData="topThree.stock" />
      </div>
    </div>
    <div class="chart-section">
      <div class="chart-card">
        <h3 class="chart-title">실시간 급등 종목</h3>
        <HighVolumeTradingStockChart :stockData="topFluctuationStocks" />
      </div>
      <div class="chart-card">
        <h3 class="chart-title">실시간 거래량 순위</h3>
        <RisingStockChart :stockData="topTransactionStocks" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance';
import { ref, computed, onMounted } from 'vue';
import PopularDepositChart from '@/components/chart/PopularDepositChart.vue';
import PopularSavingChart from '@/components/chart/PopularSavingChart.vue';
import PopularStockChart from '@/components/chart/PopularStockChart.vue'; 
import HighVolumeTradingStockChart from '@/components/chart/HighVolumeTradingStockChart.vue';
import RisingStockChart from '@/components/chart/RisingStockChart.vue';

const store = useFinanceStore();
const userProduct = ref([]);
const stocks = ref([]);
const dataLoaded = ref(false);
const loading = ref(true);

onMounted(async () => {
  try {
    await store.createUserProduct();
    await store.createStockList();
    userProduct.value = store.userProduct;
    stocks.value = removeDuplicateStocks(store.stocks)
    dataLoaded.value = true;
  } catch (error) {
    console.error("Error loading data:", error);
  } finally {
    loading.value = false;
  }
});

const topThree = computed(() => {
  if (!dataLoaded.value) {
    return {
      deposit: [],
      saving: [],
      stock: []
    };
  }

  return {
    deposit: calculateTopThree('deposit'),
    saving: calculateTopThree('saving'),
    stock: calculateTopThree('stock')
  };
});

function calculateTopThree(field) {
  if (!Array.isArray(userProduct.value) || !userProduct.value.length) {
    return [];
  }
  const values = userProduct.value.map(item => item[field]).filter(value => value && value !== 'None');
  const valueCount = {};
  values.forEach(value => {
    valueCount[value] = (valueCount[value] || 0) + 1;
  });
  const sortedValues = Object.keys(valueCount).sort((a, b) => valueCount[b] - valueCount[a]);
  return sortedValues.slice(0, 3).map(value => ({ name: value, count: valueCount[value] }));
}

// 주식 종목의 중복을 제거
const removeDuplicateStocks = (stocks => {
  const uniqueStocks = []
  const seenPrdtCd = new Set()

  for (const stock of stocks) {
    if (!seenPrdtCd.has(stock.prdt_cd)) {
      uniqueStocks.push(stock)
      seenPrdtCd.add(stock.prdt_cd)
    }
  }
  return uniqueStocks
})

// 주가 상승 top5
const topFluctuationStocks = computed(() => {
  if (!dataLoaded.value) {
    return [];
  }
  
  return stocks.value
    .filter(item => item.fluctuation_rate !== null && item.fluctuation_rate !== 'None')
    .sort((a, b) => b.fluctuation_rate - a.fluctuation_rate)
    .slice(0, 5)
    .map(item => ({ name: item.prdt_name, count: item.fluctuation_rate }));
});

// 거래량 top5
const topTransactionStocks = computed(() => {
  if (!dataLoaded.value) {
    return [];
  }
  return stocks.value
    .filter(item => item.trade_amount !== null && item.trade_amount !== 'None')
    .sort((a, b) => b.trade_amount - a.trade_amount)
    .slice(0, 5)
    .map(item => ({ name: item.prdt_name, count: item.trade_amount }));
});
</script>

<style scoped>
.stock-main {
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 20px;
}

.section-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.chart-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-bottom: 20px
}

.chart-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
  max-width: 500px;
}

.chart-title {
  margin-bottom: 10px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}
</style>