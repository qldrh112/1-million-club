<template>
    <HeaderVue />
    <div class="content-wrapper">
      <div class="recommendation-container">
        <div class="recommendation-column">
          <h2>인공지능이 나에게 맞는 상품을 추천합니다.</h2>
          <AIRecommendations :recommend="recommendList.best_recommend"/>
        </div>
        <div class="separator"></div>
          <div class="recommendation-column">
            <h2>나와 비슷한 사람은 아래 상품에 투자했어요!</h2>
            <SimilarUserRecommendations :recommend="recommendList.filter_recommend"/>
          </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useUserStore } from '@/stores/user';
  import HeaderVue from '@/components/Header.vue';
  import { ref, onMounted } from 'vue';
  import AIRecommendations from '@/components/recommendation/AIRecommendations.vue';
  import SimilarUserRecommendations from '@/components/recommendation/SimilarUserRecommendations.vue';
  
  const store = useUserStore()
  const recommendList = store.recommendList
  const dataLoaded = ref(false);
  
  onMounted(async () => {
    recommendList.value = store.recommendList;
    dataLoaded.value = true;
  });
  </script>
  
  <style scoped>
  .content-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    min-height: 80vh;
    padding: 20px;
  }
  
  .recommendation-container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    max-width: 1000px;
    width: 100%;
  }
  
  .recommendation-column {
    flex: 1;
  }
  
  .separator {
    width: 2px;
    height: 100%;
    background-color: #212121;
    margin: 0 20px;
  }
  
  .analysis-view {
    margin-top: 40px;
    max-width: 1000px;
    width: 100%;
  }
  
  .analysis-view h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  /* Add any additional styles here */
  </style>
  