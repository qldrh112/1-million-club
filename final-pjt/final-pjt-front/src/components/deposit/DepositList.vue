<template>
    <div
    class="deposit-card"
    @click="() => showDetail(deposit.fin_prdt_cd)"
    :ref="deposit.fin_prdt_cd === selectedDeposit ? 'depositElement' : null"
    >
        <h4>{{ deposit.fin_prdt_nm }}</h4>
        <DepositDetail v-if="selectedDeposit === deposit.fin_prdt_cd"
        :depositId="deposit.fin_prdt_cd"
        :deposit="deposit" 
        />
        <hr>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useFinanceStore } from '@/stores/finance';
import DepositDetail from '@/components/deposit/DepositDetail.vue';

defineProps({
    deposit: Object,
})

const store = useFinanceStore()
const selectedDeposit = ref(null)
const depositId = ref(store.depositId)
const depositElement = ref(null)

const showDetail = (async depositId => {
    // 다시 누르면 닫기
    if (selectedDeposit.value === depositId) {
        selectedDeposit.value = null
    } else {
        selectedDeposit.value = depositId
        store.depositId = null
        // 스크롤 위치 조정
        await nextTick()
        if (depositElement.value) {
            depositElement.value.scrollIntoView({ behavior: 'smooth' })
        }
    }
})

onMounted(() => {
    showDetail(depositId.value)
})

</script>

<style scoped>
.deposit-card {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.deposit-card:hover {
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