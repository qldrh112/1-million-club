<template>
  <div class="deposit-option">
    <p v-if=" depositOption.intr_rate_type==='S'">이자 방식: 단리</p>
    <p v-else-if=" depositOption.intr_rate_type==='M'">이자 방식: 복리</p>
    <p>금리: 연 {{ depositOption.intr_rate }}%</p>
    <p>최고 우대 금리: 연 {{ depositOption.intr_rate2 }}%</p>
    <p>만기: {{ depositOption.save_trm }}개월</p>
    <hr>
  </div>
</template>

<script setup>
defineProps({
  depositOption: Object,
})
</script>

<style scoped>
.deposit-option {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.deposit-option:hover {
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