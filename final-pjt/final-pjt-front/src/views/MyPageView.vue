<template>
    <HeaderVue />
    <div>
        <h1>{{ userStore.name }}님의 포트폴리오</h1>
        <Myportfolio
        :userPortfolio="userPortfolio"/>
    </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user';
import { useFinanceStore } from '@/stores/finance';
import Myportfolio from '@/components/portfolio/MyPortfolio.vue';
import HeaderVue from '@/components/Header.vue';

const userStore = useUserStore()
const store = useFinanceStore()
const userPortfolio = ref()

const getUserPortfolio = (() => {
    axios({
        method: 'post',
        url: `${store.API_URL}/myportfolio/`,
        data: {
            username: userStore.name,
        }
    }).then(res => {
        userPortfolio.value = res.data
    }).catch(err => console.log(err))
})


onMounted(getUserPortfolio)


</script>

<style scoped>
h1 {
    color: #212121;
    font-size: 2em;
    text-align: center;
    margin-top: 20px;
}
</style>