<template>
    <HeaderVue />
    <div class="container">
        <h1>적금 리스트</h1>
        <form @submit.prevent="keywordSearch">
            <input type="text" v-model="searchTerm" placeholder="검색어를 입력하세요">
            <input type="submit" value="검색">
        </form>
        <p>총 {{ savingList.length }}개가 검색되었습니다.</p>
        <div class="saving-list">
            <SavingList
            v-for="saving in savingList"
            :key="saving.fin_prdt_cd"
            :saving="saving"
            />
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue'
import { useFinanceStore } from '@/stores/finance';
import SavingList from '@/components/saving/SavingList.vue';
import HeaderVue from '@/components/Header.vue';

const store = useFinanceStore()
const savingList = ref([])
const searchTerm = ref('')

const getSavings = (() => {
    axios({
        method: 'get',
        url: `${store.API_URL}/saving/`
    }).then((res) => {
        savingList.value = res.data
}).catch((err) => console.log(err))
})

onMounted(() => { 
    getSavings()
})

const keywordSearch = () => {
    axios({
        method: 'POST',
        url: `${store.API_URL}/saving/`,
        data: {
            term: searchTerm.value,
        }
    }).then(res => {
        savingList.value = res.data
        searchTerm.value = ''
    }).catch(err => console.log(err))
}

</script>

<style scoped>
.container {
  max-width: 1500px;
  margin: auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #212121;
  font-size: 2em;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

form {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

form input[type="text"] {
  padding: 10px;
  border: 1px solid #DEDEDE;
  border-radius: 5px;
  width: 100%;
  max-width: 300px;
}

form input[type="submit"] {
  background-color: #A5C9FF;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

form input[type="submit"]:hover {
  background-color: #6b7eff;
}

p {
  color: #212121;
  text-align: center;
  margin-bottom: 20px;
}

.saving-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>