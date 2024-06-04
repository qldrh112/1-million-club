<template>
    <div class="card">
        <article class="card-body">
            <h5 class="card-title">{{ deposit.options.product.fin_prdt_nm }} - {{ deposit.options.product.kor_co_nm }}</h5>
            <main class="card-text">
                <!-- 단리 -->
                <p v-if="deposit.options.intr_rate_type === 'S'">만기 예상 이자: {{ Number(deposit.options.save_trm / 12 * (IRAT / 100 * deposit.payment)).toLocaleString() }}원</p>
                <!-- 복리 -->
                <p v-else>만기 예상 이자: {{ Number(deposit.payment * Math.pow(1 + IRAT / 100 / 12, deposit.options.save_trm)).toFixed(2) }}원</p>
                <p>가입 날짜: {{ deposit.join_date }}</p>
                <p>만기일: {{ maturity }}</p>
                <p>납입액: {{ Number(deposit.payment).toLocaleString() }}원</p>
                <p>이자율: {{ deposit.options.is_prime_rate ? deposit.options.intr_rate : deposit.options.intr_rate2 }}%</p>
                <p>세후 이자율: {{ IRAT }}%</p>
            </main>
            <button @click="goDetail(deposit.fin_prdt_cd)" class="btn btn-primary">상세 정보</button>
        </article>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useFinanceStore } from '@/stores/finance';

defineProps({
    deposit: Object,
    maturity: String,
    IRAT: Number,
})

const store = useFinanceStore()
const router = useRouter()

const goDetail = (depositId => {
    store.depositId = depositId
    router.push({ name: 'deposit' })
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
    margin: 5px;
}

.card-title {
    border-bottom: 1px solid #DEDEDE; /* 타이틀과 텍스트를 시각적으로 분리합니다. */
    padding-bottom: 10px;
    margin-bottom: 10px;
}
</style>