<template>
    <div>
        <div class="container">
            <div v-if="userPortfolio" class="user-info">
                <h3>사용자 정보</h3>
                <div class="user-info-container">
                    <p><span>연수:</span> {{ userPortfolio.portfolio_base.year }}년</p>
                    <p><span>목표 금액:</span> {{ Number(userPortfolio.portfolio_base.target).toLocaleString() }}원</p>
                    <p><span>포트폴리오 총 가치: {{ Number(userPortfolio.deposits.reduce((total, deposit) => total + deposit.payment, 0) + userPortfolio.savings.reduce((total, saving) => total + saving.monthly_payment, 0) + calculateStocksTotal(userPortfolio.stocks)).toLocaleString()}}원</span></p>
                    <p><span>투자 가능액:</span> {{ Number(userPortfolio.portfolio_base.seed_money).toLocaleString() }}원</p>
                    <p><span>월급여:</span> {{ Number(userPortfolio.portfolio_base.salary).toLocaleString() }}원</p>
                    <p><span>주거래 은행:</span> {{ userPortfolio.portfolio_base.kor_co_nm }}</p>
                    <p><span>선호 산업:</span> {{ userPortfolio.portfolio_base.industry }}</p>
                    
                </div>
            </div>
            <div class="investment-tendency">
                <h3>투자 성향</h3>
                <div v-if="userPortfolio" class="chart-wrapper">
                  <InvestmentTendencyChart
                      :investAggresive="userPortfolio.portfolio_base.invest_aggresive"
                      :investConservative="userPortfolio.portfolio_base.invest_conservative"
                  />
                </div>
            </div>
        </div>
        <h3>예금 상품 목록</h3>
        <p v-if="userPortfolio && userPortfolio.deposits"><span>예금 총액: </span>{{ userPortfolio.deposits.reduce((total, deposit) => total + deposit.payment, 0).toLocaleString() }}원</p>
        <div class="row">
            <MyportfolioDeposit v-if="userPortfolio"
            v-for="deposit in userPortfolio.deposits"
            :key="deposit.options.fin_co_no"
            :deposit="deposit" 
            :maturity="calculateMaturity(deposit.join_date, deposit.options.save_trm)"
            :IRAT="intrRate(deposit.is_prime_rate, deposit.options.intr_rate, deposit.options.intr_rate2)"
            class="col-md-3"
            />

            <h3>적금 상품 목록</h3>
            <p v-if="userPortfolio && userPortfolio.savings"><span>적금 총액: </span>{{ userPortfolio.savings.reduce((total, saving) => total + saving.monthly_payment, 0).toLocaleString() }}원</p>
            <MyportfolioSaving
            v-if="userPortfolio"
            v-for="saving in userPortfolio.savings"
            :key="saving.options.fin_co_no"
            :saving="saving"
            :maturity="calculateMaturity(saving.join_date, saving.options.save_trm)"
            :IRAT="intrRate(saving.is_prime_rate, saving.options.intr_rate, saving.options.intr_rate2)"
            class="col-md-3"
            />

            <h3>매수 증권 목록</h3>
            <p v-if="userPortfolio && userPortfolio.stocks"><span>증권 총액: </span>{{ calculateStocksTotal(userPortfolio.stocks).toLocaleString() }}원</p>
            <MyportfolioStock
            v-if="userPortfolio" 
            v-for="stock in userPortfolio.stocks"
            :key="stock.stock"
            :stock="stock" 
            class="col-md-3"
            />
        </div>
    </div>
</template>

<script setup>
import InvestmentTendencyChart from '@/components/portfolio/InvestmentTendencyChart.vue';
import MyportfolioDeposit from '@/components/portfolio/MyPortfolioDeposit.vue'
import MyportfolioSaving from '@/components/portfolio/MyPortfolioSaving.vue'
import MyportfolioStock from '@/components/portfolio/MyPortfolioStock.vue';

import { useFinanceStore } from '@/stores/finance';

defineProps({
    userPortfolio: Object,
})

const store = useFinanceStore()
function calculateMaturity(join_date, save_trm) {
    // join_date를 Date 객체로 변환합니다.
    let date = new Date(join_date);

    // save_trm를 정수로 변환하고, 이를 join_date의 월에 더합니다.
    date.setMonth(date.getMonth() + parseInt(save_trm));

    // date를 yyyy-mm-dd 형식의 문자열로 변환합니다.
    return date.toISOString().slice(0, 10);
}

// 우대금리 적용 여부에 따라서 적용 금리를 결정합니다.
const intrRate = ((isPrimeRate, intrRate, intrRate2) => {
    if (isPrimeRate) {
        return Number((intrRate2 * (1 - store.INTEREST_INCOME_TAX)).toFixed(2))
    } else {
        return Number((intrRate * (1 - store.INTEREST_INCOME_TAX)).toFixed(2))
    }
})

// const savingIntrRate = computed(() => {
//     return saving.options.is_prime_rate ? saving.options.intr_rate : saving.options.intr_rate2
// })
const calculateStocksTotal = (stocks) => {
    return stocks.reduce((total, stock) => {
        // 각 주식의 총액을 계산하여 더함
        return total + (stock.product.end_price * stock.amount);
    }, 0);
}
</script>

<style scoped>
.container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px; /* 컴포넌트 위아래 간격을 조정합니다. */
}
.user-info, .investment-tendency {
    width: 45%;
}

.user-info {
    font-size: 1.2em;
}

.user-info-container p {
    margin: 40px 0;
}

.investment-tendency {
    font-size: 1.2em;
}

h3 {
    color: #212121;
    font-size: 1.5em;
    text-align: center;
    margin-top: 20px;
}

.chart-wrapper {
    width: 80%; /* 차트의 크기를 20% 줄임 */
    height: auto; /* 높이 자동 조절 */
}

.row {
    margin: 0 -15px; /* 컴포넌트 간의 간격을 조정합니다. */
    display: flex;
    justify-content: center; /* 자식 요소를 수평으로 중앙 정렬합니다. */
}

.card-container {
    margin: 10px; /* 카드 간의 간격을 조정합니다. */
}

.col-md-4 {
    /* 각 상품 카드의 너비를 조정합니다. */
    width: 30%; /* 원하는 너비로 조정해주세요. */
    padding: 0 15px;
}
</style>