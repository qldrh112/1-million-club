<template>
  <div class="stock-detail">
      <RouterLink :to="{ name : 'coperation', params: {'coperationname':stock.prdt_name} }">상세기업정보</RouterLink>
      <p>종목 코드: {{ stock.prdt_cd }}</p>
      <p>종가: {{ Number(stock.end_price).toLocaleString() }}원</p>
      <p>전일대비 등락률: {{ stock.fluctualtion_rate }}%</p>
      <p>거래량: {{ Number(stock.trade_amount).toLocaleString() }}건</p>
      <p>거래액: {{ Number(stock.trade_price_amount).toLocaleString() }}원</p>
      <p>시가총액: {{ Number(stock.capitalization).toLocaleString() }}원</p>
      <p>유통 주식 수: {{ Number(stock.shared_amount).toLocaleString() }}주</p>
      <p>산업분류: {{ stock.idx_bztp_mcls_cd_name }}</p>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  stock: Object
})
</script>

<style scoped>
.stock-detail {
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
