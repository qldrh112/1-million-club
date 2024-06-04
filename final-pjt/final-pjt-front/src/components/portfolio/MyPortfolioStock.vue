<template>
    <div class="card">
        <article class="card-body">
            <h5 class="card-title">{{ stock.product.prdt_cd }} - {{ stock.product.prdt_name }}</h5>
            <main class="card-text">
                <p>현재가: {{ Number(stock.product.end_price).toLocaleString() }}원</p>
                <p>보유 수량: {{ Number(stock.amount).toLocaleString() }}주</p>
                <p>평가 가치: {{ Number(stock.amount * stock.product.end_price).toLocaleString() }}원</p>
            </main>
            <button class="btn btn-primary" @click="goDetail(stock.prdt_cd)">상세 정보</button>
        </article>
    </div>
</template>



<script setup>
import { useRouter } from 'vue-router';
import { useFinanceStore } from '@/stores/finance';
defineProps({
    stock: Object,
})

const store = useFinanceStore()
const router = useRouter()
const goDetail = (stockId => {
    store.stockId = stockId
    router.push({ name: 'stock' })
})
</script>

<style scoped>
div {
    border: 1px solid #DEDEDE;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
}

p {
    color: #212121;
    margin-left: 10px;
}

p span {
    color: #A5C9FF;
}

button {
    background-color: #A5C9FF;
    color: #212121;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    margin-top: 10px;
}

button:hover {
    background-color: #212121;
    color: #A5C9FF;
}

.card {
    border: 1px solid #DEDEDE;
    border-radius: 5px;
    padding: 10px;
    margin: 5px; /* 카드 간의 간격을 조금 벌립니다. */
}

.card-title {
    border-bottom: 1px solid #DEDEDE; /* 타이틀과 텍스트를 시각적으로 분리합니다. */
    padding-bottom: 10px;
    margin-bottom: 10px;
}
</style>