<template>
  <div>
    <div class="header">
      <h1 @click="gohome" class="logo">1억 클럽</h1>
      <div class="auth-links" v-if="!store.isLogin">
          <RouterLink :to="{ name: 'signUp' }">회원가입</RouterLink>
          <span> | </span>
          <RouterLink :to="{ name: 'signIn' }">로그인</RouterLink>
      </div>
      <div v-else class="auth-links">
        <RouterLink :to="{name: 'myPage', params:{userId: store.name}}">마이페이지</RouterLink>
        <span> | </span>
        <RouterLink :to="{name: 'passwordChange'}">비밀번호 변경</RouterLink>
        <span> | </span>
        <a @click="logout">로그아웃</a>
      </div>
    </div>
    <nav class="nav-container">
      <div class="nav-links">
        <RouterLink :to="{ name: 'stock' }">주식</RouterLink>
        <span> | </span>
        <RouterLink :to="{ name: 'deposit' }">예금</RouterLink>
        <span> | </span>
        <RouterLink :to="{ name: 'saving' }">적금</RouterLink>
        <span> | </span>
        <RouterLink :to="{ name: 'inputUserInfo' }" v-if="store.isLogin">포트폴리오 추천 받기</RouterLink>
      </div>
    </nav>
  </div>
</template>
  
<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const store = useUserStore();

const gohome = () => {
  router.push({ name: 'home' });
};

const logout = () => {
  store.logout();
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #212121;
  color: #DEDEDE;
}

.logo {
  font-size: 2.5rem;
  font-weight: bold;
  cursor: pointer;
  color: #9DDFFF;
  text-align: center;
}

.auth-links {
  display: flex;
  gap: 0.5rem;
}

.auth-links a,
.auth-links .router-link {
  color: #A5C9FF;
  text-decoration: none;
}

.auth-links a:hover,
.auth-links .router-link:hover {
  text-decoration: underline;
}

.nav-container {
  display: flex;
  justify-content: center;
  background-color: #212121;
  padding: 1rem 0;
}

.nav-links {
  display: flex;
  gap: 5rem;
}

.nav-links a,
.nav-links .router-link {
  color: #fff; /* 링크 색상 */
  text-decoration: none; /* 링크 밑줄 제거 */
}

.nav-links a:hover,
.nav-links .router-link:hover {
  text-decoration: underline; /* 호버 시 링크 밑줄 추가 */
}
</style>
