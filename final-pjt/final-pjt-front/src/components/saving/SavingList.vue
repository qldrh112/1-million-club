
<template>
    <div
    class="saving-card"
    @click="() => showDetail(saving.fin_prdt_cd)" 
    :ref="saving.fin_prdt_cd === selectedSaving ? 'savingElement' : null"
    >
        <h4>{{ saving.fin_prdt_nm }}</h4>
        <SavingDetail v-if="selectedSaving === saving.fin_prdt_cd"
        :savingId="saving.fin_prdt_cd"
        :saving="saving" 
        />
        <hr>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useFinanceStore } from '@/stores/finance';
import SavingDetail from '@/components/saving/SavingDetail.vue';

defineProps({
    saving: Object,
})

const store = useFinanceStore()
const selectedSaving = ref(null)
const savingId = ref(store.savingId)
const savingElement = ref(null)

const showDetail = (async savingId => {
    // 다시 누르면 닫기
    if (selectedSaving.value === savingId) {
        selectedSaving.value = null
    } else {
        selectedSaving.value = savingId
        store.savingId = null
        // 스크롤 위치 조정
        await nextTick()
        if (savingElement.value) {
            savingElement.value.scrollIntoView({ behavior: 'smooth' })
        }
    }
})

onMounted(() => {
    showDetail(savingId.value)
})
</script>

<style scoped>
.saving-card {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.saving-card:hover {
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