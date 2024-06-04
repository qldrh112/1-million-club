<template>
  <HeaderVue />
        <!-- 로딩 상태일 때 로딩 창 표시 -->
    <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
    </div>
    <div v-if="store.isLogin">
        <br>
        <h3>정보를 입력해 주세요.</h3>
        <form @submit.prevent="inputUserInfo">
        <div class="form-group">
            <label for="targetYear">연도 </label><br>
            <input type="radio" id="oneYear" value="1" v-model="targetYear" required>
            <label for="oneYear">1년</label>
            <input type="radio" id="twoYears" value="2" v-model="targetYear" required>
            <label for="twoYears">2년</label>
            <input type="radio" id="threeYears" value="3" v-model="targetYear" required>
            <label for="threeYears">3년</label>
        </div>

        <div class="form-group">
            <label for="targetWealth">목표 금액: </label><br>
            <input id="targetWealth" type="number" min="0" max="1000000000" step="1000000" v-model.number="targetWealth" required>
            <span>원</span><br>
        </div>

        <div class="form-group">
            <label for="invest-aggresive">위험 선호도</label><br>
            <span>위험 회피</span><input id="seedMoney" type="range" min="0" max="100" step="10" v-model.number="investAggresive"><span>위험 수용</span>
            <p>{{ investAggresive }}</p>
        </div>

        <div class="form-group">
            <label for="seedMoney">투자 자본: </label>
            <input id="seedMoney" type="number" min="0" max="1000000000" step="1000000" v-model.number="seedMoney" required>
            <span>원</span><br>
            <p class="input-info">최대 10억까지 입력 가능합니다.</p>
        </div>

        <div class="form-group">
            <label for="salary">월 급여: </label>
            <input id="salary" type="number" min="0" max="10000000" step="1000" v-model.number="salary" required>
            <span>원</span><br>
            <p class="input-info">최대 천만원까지 입력 가능합니다.</p>
        </div>
        <div class="form-group">
            <label for="age">나이: </label>
            <input id="age" type="number" min="19" max="120" v-model.number="age" required>
            <span>세</span><br>
        </div>
        <div class="form-group">
            <label for="industry">관심 산업: </label>
            <!-- 산업군 입력창을 클릭하면 openModal 함수를 호출합니다. -->
            <input type="text" id="industry" v-model="industry" @click="openModal" required><br> 
        </div>
            <div v-if="showModal" class="modal">
                <div class="modal-content">
                    <!-- 취소 버튼을 클릭하면 closeModal 함수를 호출합니다. -->
                    <span class="close" @click="closeModal">&times;</span> 
                    <input type="text" v-model="searchTerm" @input="searchIndustry" required>
                    <div v-for="(industry, index) in filteredIndustryList" :key="index" @click="selectIndustry(industry)">{{ industry }}</div>
                </div>
            </div>
            
        <label for="kor-co-nm">주거래 은행</label>
        <div class="bank-list-container">
            <div v-for="(bank, index) in bankList" :key="index" class="bank-list">
                <button :class="{ active: korCoNm === bank }" @click.prevent="selectBank(bank)">{{ bank }}</button>
            </div>

        </div>

        <div class="form-group">
            <label for="isPrimeRate">우대 금리 적용</label>
            <input id="isPrimeRate" type="checkbox" v-model="isPrimeRate"><br>
        </div>

            <input type="submit" value="분석하기">
            <br>
            <br>
            <br>
        </form>
    </div>
</template>

<script setup>
import HeaderVue from '@/components/Header.vue';
import { watch, ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user';
import axios from 'axios';


const store = useUserStore()

const bankList = ref(null)
const industryList = ref(null)

const targetYear = ref(null)
const targetWealth = ref(null)
const seedMoney = ref(null)
const investAggresive = ref(50)
const investConservative = ref(50)

const loading = ref(false)

watch(investAggresive, () => {
    investConservative.value = 100 - investAggresive.value
})

const salary = ref(null)
const age = ref(null)
const industry = ref(null)
const korCoNm = ref(null)
const isPrimeRate = ref(false)

const inputUserInfo = (() => {
    loading.value = true; // 폼 제출 시 로딩 상태를 true로 변경
    const payload = {
        targetYear: Number(targetYear.value),
        targetWealth: Number(targetWealth.value),
        seedMoney: Number(seedMoney.value),
        investAggresive: Number(investAggresive.value),
        investConservative: Number(investConservative.value),
        salary: Number(salary.value),
        age: Number(age.value),
        industry: industry.value,
        korCoNm: korCoNm.value,
        isPrimeRate: isPrimeRate.value,
    }
    store.createUserInfo(payload)
    
})

const selectBank = (bank) => {
    korCoNm.value = bank
    
}

const selectIndustry = (selectedIndustry) => {
    industry.value = selectedIndustry // 선택한 industry 값을 입력창에 설정합니다.
    closeModal() // 모달을 닫습니다.
}

const showModal = ref(false) // 모달을 보여줄지 말지 결정하는 변수를 추가합니다.

const openModal = () => {
    showModal.value = true // 산업군 입력창을 클릭하면 모달을 보여줍니다.
}

const closeModal = () => {
    showModal.value = false // 취소 버튼을 클릭하면 모달을 숨깁니다.
}

const searchTerm = ref('')
const filteredIndustryList = computed(() => {
    if (!searchTerm.value) {
        return industryList.value
    }
    return industryList.value.filter(industry => industry.includes(searchTerm.value))
})

onMounted(() => {
    axios({
        method: 'get',
        url: `${store.API_URL}/banks/`
    }).then(res => {
        bankList.value = res.data
        axios({
            method: 'get',
            url: `${store.API_URL}/industries/`
        }).then(res => {
            industryList.value = res.data
        }).catch(err => console.log(err))
    }).catch(err => console.log(err))
})
</script>

<style scoped>

/* 은행 스크롤 추가 */
.bank-list-container {
  max-height: 500px; /* 최대 높이 지정 */
  overflow-y: auto; /* 세로 스크롤을 표시하는 스크롤 영역 생성 */
}
/* 폼 요소 간의 간격을 유지하기 위해 form-group 클래스를 추가합니다. */
.form-group {
  margin-bottom: 15px;
}

/* 연도 라디오 버튼 간의 거리를 유지하기 위해 margin-right를 추가합니다. */
label {
  margin-right: 10px;
}

/* 최대 입력 가능 금액 안내 문구의 스타일을 수정합니다. */
.input-info {
  font-size: 14px;
  color: #888;
}

/* 은행 선택을 한 행에 여러 개씩 배치하기 위해 Flexbox를 사용합니다. */
.bank-list {
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center; /* 버튼들을 중앙 정렬합니다. */
}

/* 각 버튼 사이의 간격을 조정합니다. */
.bank-list button {
  margin: 5px; /* 상하좌우 여백 조정 */
}

/* 모달의 스타일을 수정하여 가이드에 맞춥니다. */
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.active {
    background-color: black;
    content: ' ✓';
}

.loading-overlay {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>