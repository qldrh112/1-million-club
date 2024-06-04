<template>
    <HeaderVue />
    <div class="password-change-container">
        <h1>비밀번호 변경</h1>
        <form @submit.prevent="passwordChange">
            <label for="password1">새 비밀번호</label>
            <input type="password" id="password1" v-model="password1"><br>
            <label for="password2">비밀번호 확인</label>
            <input type="password" id="password2" v-model="password2"><br>
            <input type="submit" value="비밀번호 변경">
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import HeaderVue from '@/components/Header.vue';

const store = useUserStore()
const password1 = ref(null)
const password2 = ref(null)

const passwordChange = (() => {
    const payload = {
        password1: password1.value,
        password2: password2.value
    }
    store.passwordChange(payload)  
})
</script>

<style scoped>
.password-change-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 100px);
}

h1 {
    color: #212121;
    font-size: 2.5em;
    text-align: center;
    margin-bottom: 30px;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    width: 100%;
    max-width: 500px;
}

label {
    color: #212121;
    font-size: 1.2em;
    align-self: flex-start;
    margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
    padding: 15px;
    border: 1px solid #DEDEDE;
    border-radius: 5px;
    width: 100%;
    font-size: 1.2em;
}

input[type="submit"] {
    background-color: #A5C9FF;
    color: #212121;
    border: none;
    border-radius: 5px;
    padding: 15px 20px;
    cursor: pointer;
    width: 100%;
    font-size: 1.2em;
}

input[type="submit"]:hover {
    background-color: #212121;
    color: #A5C9FF;
}
</style>