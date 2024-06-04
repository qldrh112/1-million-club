<template>
    <HeaderVue />
    
    <div class="content-wrapper">
        <div v-if="loading" class="loading-message">
            기업정보 로딩 중...
        </div>
        <div v-else-if="coperationdetail[0]" class="stock-option">
            <h1>{{ coperationdetail[0].corpNm }}</h1>
            <h3>{{ coperationdetail[0].corpEnsnNm }}</h3>
            <p v-if="coperationdetail[0].enpMainBizNm">주요사업 : {{ coperationdetail[0].enpMainBizNm }}</p>
            <p v-if="coperationdetail[0].crno">법인 등록번호 : {{ coperationdetail[0].crno }}</p>
            <p v-if="coperationdetail[0].enpRprFnm">대표자명 : {{ coperationdetail[0].enpRprFnm }}</p>
            <p v-if="coperationdetail[0].bzno">사업자등록번호 : {{ coperationdetail[0].bzno }}</p>
            <p v-if="coperationdetail[0].enpDtadr">기업상세주소 : {{ coperationdetail[0].enpDtadr }}</p>
            <p v-if="homePage">홈페이지 주소 : <a :href="homePage" target="_blank">{{ homePage }}</a></p>
            <p v-if="coperationdetail[0].enpTlno">대표전화번호 : {{ coperationdetail[0].enpTlno }}</p>
            <p v-if="coperationdetail[0].sicNm">표준산업분류명 : {{ coperationdetail[0].sicNm }}</p>
            <p v-if="coperationdetail[0].enpEstbDt">기업설립일자 : {{ coperationdetail[0].enpEstbDt }}</p>
            <p v-if="coperationdetail[0].enpEmpeCnt">종업원수 : {{ Number(coperationdetail[0].enpEmpeCnt).toLocaleString() }}명</p>
            <p v-if="coperationdetail[0].empeAvgCnwkTermCtt">평균근속연수 : {{ coperationdetail[0].empeAvgCnwkTermCtt }}년</p>
            <p v-if="coperationdetail[0].enpPn1AvgSlryAmt">평균 급여액 : {{ Number(coperationdetail[0].enpPn1AvgSlryAmt).toLocaleString() }}원</p>
            <RouterLink :to="{name: 'stock'}">뒤로 가기</RouterLink>
            <CorporationAccountingInfo />
        </div>
        <div v-else class="error-message">
            기업정보를 찾을 수 없습니다.
            <RouterLink :to="{name: 'stock'}">뒤로 가기</RouterLink>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import CorporationAccountingInfo from '@/components/CorporationAccountingInfo.vue';
import HeaderVue from '@/components/Header.vue';

const route = useRoute()
const coperationname = route.params.coperationname
const coperationdetail = ref([])
const loading = ref(true);
const homePage = ref('')

const Financ_URL = 'https://apis.data.go.kr/1160100/service/GetCorpBasicInfoService_V2/getCorpOutline_V2?ServiceKey=OJmj4wS5CMF3cl%2B4ODaGPyKkMpMli6byx9RJZJwJoBg0%2FUJUtRPab5nG61mITe2A7lT6Q7%2Fplh9oAiEOpQftvQ%3D%3D&pageNo=1&numOfRows=1&resultType=json&corpNm='
onMounted(() => {
    axios({
        method: 'get',
        url: `${Financ_URL}${coperationname}`
    })
    .then((response) => {
        coperationdetail.value = response.data.response.body.items.item
        let url = coperationdetail.value[0].enpHmpgUrl
        console.log(url)
        homePage.value = url.startsWith('http://') || url.startsWith('https://') ? url : 'https://' + url;
        loading.value = false
    })
    .catch((error) => {
        console.log(error)
        loading.value = false
    });
});
</script>

<style scoped>
.content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh; /* Center vertically */
    padding: 20px;
}

.back-navigation {
    margin-bottom: 20px;
    text-align: center;
}

.back-navigation a {
    color: #A5C9FF;
    text-decoration: none;
    font-weight: bold;
}

.back-navigation a:hover {
    text-decoration: underline;
}

.loading-message, .error-message {
    color: #212121;
    font-size: 1.2em;
    text-align: center;
}

.stock-option {
  border: 1px solid #DEDEDE;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  transition: background-color 0.3s ease;
  max-width: 800px;
  width: 100%;
}

p {
  color: #212121;
  margin-left: 10px;
  margin-bottom: 10px;
}

a {
  color: #A5C9FF;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
