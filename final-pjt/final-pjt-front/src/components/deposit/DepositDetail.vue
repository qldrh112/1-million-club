<template>
    <div class="deposit-detail">
        <p>{{ deposit.kor_co_nm }}</p>
        <p v-if="deposit.max_limit">한도: {{ Number(deposit.max_limit).toLocaleString() }}원</p>
        <p>가입 방법: {{ deposit.join_way }}</p>
        <p v-if="deposit.join_deny===2">가입 제한: 서민 전용</p>
        <p v-else-if="deposit.join_deny===3">가입 제한: 일부 제한</p>
        <p>가입 대상: {{ deposit.join_member }}</p>
        <p v-if="deposit.join_spcl_cnd">우대사항: {{ deposit.join_spcl_cnd }}</p>
        <p>기타: {{ deposit.etc_note }}</p>
        <h3>옵션</h3>
        <DepositOptionList
        v-for="depositOption in deposit.depositoption_set"
        :key="depositOption.deposit"
        :depositOption="depositOption"
        />
    </div>
</template>

<script setup>
import DepositOptionList from '@/components/deposit/DepositOptionList.vue';
defineProps({
    deposit: Object
})

</script>



<style scoped>
.deposit-detail {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #f9f9f9;
}

p {
  color: #212121;
  margin-left: 10px;
  margin-bottom: 10px;
}

h3 {
  color: #212121;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 10px;
}
</style>