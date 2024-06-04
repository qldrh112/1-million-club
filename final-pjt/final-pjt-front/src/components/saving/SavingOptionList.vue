<template>
  <div class="saving-option">
    <p v-if=" savingOption.intr_rate_type==='S'">이자 방식: 단리</p>
    <p v-else-if=" savingOption.intr_rate_type==='M'">이자 방식: 복리</p>
    <p v-if=" savingOption.rsrv_type==='S'">적립 방식: 정액정립식</p>
    <p v-else-if=" savingOption.rsrv_type==='F'">적립 방식: 자유납입식</p>
    <p>금리: 연 {{ savingOption.intr_rate }}%</p>
    <p>최고 우대 금리: 연 {{ savingOption.intr_rate2 }}%</p>
    <p>만기: {{ savingOption.save_trm }}개월</p>
    <hr>
  </div>
</template>

<script setup>
defineProps({
  savingOption: Object
})
</script>

<style scoped>
.saving-option {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.saving-option:hover {
  background-color: #e0e7ff;
}

p {
  color: #212121;
  margin-left: 10px;
  margin-bottom: 10px;
}

hr {
  border-top: 1px solid #DEDEDE;
}
</style>