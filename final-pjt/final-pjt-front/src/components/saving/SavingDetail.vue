<template>
    <div class="saving-detail">
        <p>{{ saving.kor_co_nm }}</p>
        <p v-if="saving.max_limit">한도: {{ Number(saving.max_limit).toLocaleString() }}원</p>
        <p>가입 방법: {{ saving.join_way }}</p>
        <p v-if="saving.join_deny===2">가입 제한: 서민 전용</p>
        <p v-else-if="saving.join_deny===3">가입 제한: 일부 제한</p>
        <p>가입 대상: {{ saving.join_member }}</p>
        <p v-if="saving.join_spcl_cnd">우대사항: {{ saving.join_spcl_cnd }}</p>
        <p>기타: {{ saving.etc_note }}</p>
        <h3>옵션</h3>
        <SavingOptionList
        v-for="savingOption in saving.savingoption_set"
        :key="savingOption.saving"
        :savingOption="savingOption"
        />
    </div>
</template>

<script setup>
import SavingOptionList from '@/components/saving/SavingOptionList.vue';
defineProps({
    saving: Object
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