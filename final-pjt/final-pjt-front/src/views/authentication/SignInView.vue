<template>
    <HeaderVue />
    <div class="signin-container">
        <h1>로그인</h1>
        <form @submit.prevent="signIn">
            <label for="username">아이디: </label>
            <input id="username" type="text" v-model.trim="username"><br>
            <label for="password">비밀번호: </label>
            <input id="password" type="password" v-model.trim="password"><br>
            <input type="submit" value="로그인">
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user';
import HeaderVue from '@/components/Header.vue';

const store = useUserStore()
const username = ref(null)
const password = ref(null)

const signIn = () => {
    const payload = {
        username: username.value,
        password: password.value
    }
    store.signIn(payload)
}
</script>

<style scoped>
.signin-container {
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
