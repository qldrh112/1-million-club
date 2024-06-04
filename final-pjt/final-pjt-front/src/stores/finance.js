import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const API_URL =  'http://127.0.0.1:8000/finances'
  const INTEREST_INCOME_TAX = 0.154


  const stocks = ref([])
  const userProduct = ref([])
  const depositId = ref(null)
  const savingId = ref(null)
  const stockId = ref(null)

  const createStockList = function() {
    const url = `${API_URL}/stock/`

    axios({
      method: 'get',
      url: url
    })
    .then((response) => {
      stocks.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }

  const createUserProduct = function() {
    const url = `${API_URL}/user/product/`

    axios({
      method: 'get',
      url: url
    })
    .then((response) => {
      userProduct.value = response.data.result
    })
    .catch((error) => {
      console.log(error)
    })
  }

  return { API_URL, stocks, depositId, savingId, stockId, userProduct, INTEREST_INCOME_TAX, createStockList, createUserProduct }
}, { persist: true })
