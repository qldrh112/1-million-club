<template>
  <HeaderVue />
  <div class="carousel-container">
    <div class="carousel">
      <div class="carousel-inner">
        <div
          v-for="(slide, index) in slides"
          :key="index"
          :class="['carousel-item', { active: index === currentSlide }]"
        >
          <img :src="slide.image" class="d-block w-100 carousel-image" :alt="slide.alt" />
        </div>
      </div>
      <button class="carousel-control-prev" @click="prevSlide">
        <span class="carousel-control-prev-icon"></span>
      </button>
      <span class="carousel-counter">{{ currentSlide + 1 }} / {{ slides.length }}</span>
      <button class="carousel-control-next" @click="nextSlide">
        <span class="carousel-control-next-icon"></span>
      </button>
    </div>
  </div>
    <Chart />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import Chart from '@/components/chart/Chart.vue';
import HeaderVue from '@/components/Header.vue';

import image1 from '@/assets/image1.jpg';
import image2 from '@/assets/image2.jpg';
import image3 from '@/assets/image3.jpg';


const slides = ref([
  { image: image1, alt: 'Image 1' },
  { image: image2, alt: 'Image 2' },
  { image: image3, alt: 'Image 3' },
]);
const currentSlide = ref(0);

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.value.length;
};

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + slides.value.length) % slides.value.length;
};

let intervalId = null;

// const fetchGraphs = async () => {
//   try {
//     const response = await axios.get(`http://localhost:8000/finances/exchange-rates/`);
//     const graphBase64 = response.data;
//     slides.value.push({
//       image: `data:image/png;base64,${graphBase64}`,
//       alt: `Exchange Rate Graph for KRW`
//     });
//   } catch (error) {
//     console.error(`Failed to fetch exchange rate graph for KRW:`, error);
//   }
// }

onMounted(async () => {
  intervalId = setInterval(nextSlide, 3000); // 3초마다 다음 슬라이드로 전환
  // await fetchGraphs();
});

onUnmounted(() => {
  clearInterval(intervalId); // 컴포넌트가 unmount될 때 인터벌을 정리
});
</script>

<style scoped>
.carousel-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.carousel {
  position: relative;
  height: 550px;
  width: 100%;
  max-width: 1500px; /* 최대 너비 설정 */
  background-color: #f0f0f0;
}

.carousel-inner {
  height: 100%;
}

.carousel-item {
  display: none;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.carousel-item.active {
  display: flex;
}

.carousel-image {
  width: 100%;
  height: auto;
}

.carousel-control-prev,
.carousel-control-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  border: none;
  padding: 5px;
  cursor: pointer;
  width: 30px;
  height: 30px;
}

.carousel-control-prev {
  left: 10px;
}

.carousel-control-next {
  right: 10px;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: transparent;
  border: solid white;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 5px;
}

.carousel-control-prev-icon {
  transform: rotate(135deg);
}

.carousel-control-next-icon {
  transform: rotate(-45deg);
}

.carousel-counter {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
