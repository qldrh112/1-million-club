<template>
    <div
    class="stock-card"
    @click="() => showDetail(stock.prdt_cd)"
    :ref="stock.prdt_cd === selectedStock ? 'stockElement' : null"
    >
        <h4>{{ stock.prdt_name }}</h4>
        <StockDetail v-if="selectedStock === stock.prdt_cd"
        :stockId="stock.prdt_cd"
        :stock="stock" 
        />
        <hr>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useFinanceStore } from '@/stores/finance';
import StockDetail from '@/components/stock/StockDetail.vue';

defineProps({
    stock: Object,
})

const store = useFinanceStore()
const selectedStock = ref(null)
const stockId = ref(store.stockId)
const stockElement = ref(null)

const showDetail = (async stockId => {
    // 다시 누르면 닫기
    if (selectedStock.value === stockId) {
        selectedStock.value = null
    } else {
        selectedStock.value = stockId
        store.stockId = null
        // 스크롤 위치 조정
        await nextTick()
        if (stockElement.value) {
            stockElement.value.scrollIntoView({ behavior: 'smooth' })
        }
    }
})

onMounted(() => {
    showDetail(stockId.value)
})
</script>

<style scoped>
.stock-card {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.stock-card:hover {
  background-color: #e0e7ff;
}

h4 {
  color: #212121;
  text-align: center;
  margin-bottom: 10px;
}

hr {
  border-top: 1px solid #DEDEDE;
}
</style>
