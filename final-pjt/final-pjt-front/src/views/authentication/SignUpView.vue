<template>
    <HeaderVue />
    <div class="signup-container">
        <h1>회원 가입</h1>
        <form @submit.prevent="signUp">
            <label for="username">아이디: </label>
            <input type="text" id="username" v-model.trim="userName"><br>
            <!-- <label for="username">성: </label>
            <input type="text" id="firstname" v-model.trim="firstName"><br>
            <label for="username">이름: </label>
            <input type="text" id="lastname" v-model.trim="lastName"><br> -->
            <label for="email">이메일: </label>
            <input type="email" id="email" v-model.trim="email"><br>
            <label for="password1">비밀번호: </label>
            <input type="password" id="password1" v-model.trim="password1"><br>
            <label for="password2">비밀번호 확인: </label>
            <input type="password" id="password2" v-model.trim="password2"><br>
            <input type="submit" value="회원가입">
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user';
import HeaderVue from '@/components/Header.vue';

const store = useUserStore()
const userName = ref(null)
// const firstName = ref(null)
// const lastName = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const signUp = () => {
    const payload = {
        username: userName.value,
        // firstName: firstName.value,
        // lastName: lastName.value,
        email: email.value,
        password1: password1.value,
        password2: password2.value,
    }
    store.signUp(payload)
}
</script>

<style scoped>
.signup-container {
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
input[type="email"],
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
