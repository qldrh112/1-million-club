<template>
    <div class="card">
        <article class="card-body">
            <h5 class="card-title">
                {{ saving.options.product.fin_prdt_nm }} - {{ saving.options.product.kor_co_nm }}
                <span v-if="saving.options.rsrv_type === 'S'">(정액정립)</span>
                <span v-else-if="saving.options.rsrv_type === 'F'">(자유적립)</span>
            </h5>
            <main class="card-text">
                <div v-if="saving.options.rsrv_type === 'S'">
                    <!-- 단리 -->
                    <p v-if="saving.options.intr_rate_type === 'S'">만기 예상 이자: {{ Number(saving.options.save_trm / 12 * (IRAT / 100 * saving.monthly_payment)).toLocaleString() }}원</p>
                    <!-- 복리 -->
                    <p v-else>만기 예상 이자: {{ Number(saving.monthly_payment * Math.pow(1 + IRAT / 100 / 12, saving.options.save_trm)).toFixed(2) }}원</p>
                    <p>월 납입액: {{ Number(saving.monthly_payment).toLocaleString() }}원</p>
                </div>
                <p>가입날짜: {{ saving.join_date }}</p>
                <p>만기일: {{ maturity }}</p>
                <p>이자율: {{ saving.options.is_prime_rate ? saving.options.intr_rate : saving.options.intr_rate2 }}%</p>
                <p>세후 이자율: {{ IRAT }}%</p>
            </main>
            <button class="btn btn-primary" @click="goDetail(saving.fin_prdt_cd)">상세 정보</button>
        </article>
    </div>
</template>


<script setup>
import { useRouter } from 'vue-router';
import { useFinanceStore } from '@/stores/finance';

defineProps({
    saving: Object,
    maturity: String,
    IRAT: Number,
})

const store = useFinanceStore()
const router = useRouter()
const goDetail = (savingId => {
    store.savingId = savingId
    router.push({ name: 'saving' })
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