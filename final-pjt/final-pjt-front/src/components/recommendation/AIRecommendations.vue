<template>
    <div class="recommend-best">
      <p class="input-info">상품을 누르면 상세 페이지로 이동합니다.</p>
      <ul>
        <li v-for="(product, category) in recommend" :key="category">
          <p @click="goDetail(product, category)"><span >{{ category }}:</span> {{ product }}</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter()
  const props = defineProps({
    recommend: Object
  })

  const goDetail = ((product, category) => {
    if (category === '예금') {
        router.push({name: 'deposit', query: {product}})
    } else if (category === '적금') {
        router.push({name: 'saving', query: {product}}) 
    } else {
        router.push({name: 'stock', query: {product}})
    }
  })
  </script>
  
  <style scoped>
  .recommend-best {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #E4EFFF;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .recommend-best ul {
    list-style-type: none;
    padding: 0;
  }
  
  .recommend-best li {
    margin-bottom: 10px;
    color: #212121;
  }
  
  .recommend-best span {
    font-weight: bold;
    color: #2A47FF;
  }

.input-info {
  font-size: 14px;
  color: #888;
}
  </style>
  