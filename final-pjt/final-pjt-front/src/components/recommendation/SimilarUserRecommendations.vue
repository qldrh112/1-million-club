<template>
  <div class="recommend-filter">
    <ul>
      <li v-for="(list, category) in recommend" :key="category">
        <h5>{{ category }} 리스트</h5>
        <ul>
          <li v-for="product in list" :key="product">{{ product }}</li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  recommend: Object
})
</script>

<style scoped>
.recommend-filter {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #E4EFFF;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.recommend-filter ul {
  list-style-type: none;
  padding: 0;
}

.recommend-filter li {
  margin-bottom: 20px;
}

.recommend-filter h5 {
  margin-bottom: 10px;
  font-size: 1.2em;
  color: #212121;
  border-bottom: 2px solid #DEDEDE;
  padding-bottom: 5px;
}
</style>
