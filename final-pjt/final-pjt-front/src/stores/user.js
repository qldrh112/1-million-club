import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'


export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref(null)
  const name = ref(null)
  const portfolioId = ref(null)
  const isLoggedIn = ref(false)
  const recommendList = ref([])

  
  const isLogin = computed(() => {
    if (isLoggedIn.value) {
      return true
    } else {
      return false
    }
  })

const signUp = (payload => {
    const username = payload.username
    const email = payload.email
    const password1 = payload.password1
    const password2 = payload.password2
  
    // email이 제공되지 않았다면 오류를 던집니다.
    if (!email) {
      window.alert('Email is required for signup.')
      throw new Error('Email is required for signup.')
    }
  
    axios({
      method: 'post',
      url: `${API_URL}/signup/`,
      data: {
        username, email, password1, password2,
      }
    }).then(res => {
      console.log('회원가입이 완료되었습니다.')
      const password = password1
      signIn({ username, password })
    }).catch(err => {
      console.log(err.response.data)
      // 필드가 충족되지 않았을 때
      if (err.response.data.non_field_errors) {
        window.alert(err.response.data.non_field_errors[0])
      } 
      // username에 대한 오류 메시지가 있는 경우
      else if (err.response.data.username) { 
        window.alert(err.response.data.username[0])
      } else {
        window.alert('회원 가입 요청 중 오류가 발생했습니다.')
      }
    })
  })


  const signIn = (payload => {
    const username = payload.username
    const password = payload.password
    
    axios({
      method: 'post',
      url: `${API_URL}/login/`,
      data: {
        username, password,
      }
    }).then(res => {
      // 로그인 성공 - 'key'를 반환합니다.
      if (res.data.key) { 
        token.value = res.data.key
        isLoggedIn.value = true
        name.value = username
        console.log('로그인이 완료되었습니다.')
        router.push({ name: 'home' })

        // 토큰과 이름을 로컬 스토리지에 저장
        localStorage.setItem('token', res.data.key)
        localStorage.setItem('name', name.value)
      } else {
        // 로그인 실패에 대한 오류 메시지를 반환
        window.alert(res.data.non_field_errors[0])
      }
    }).catch(err => {
      console.log(err)
      if (err.response.data.non_field_errors) {
        window.alert(err.response.data.non_field_errors[0])
      } else {
        window.alert('로그인 요청 중 오류가 발생했습니다.')  
      }
    })
  })

  // 페이지 로드 시 로컬 스토리지에서 토큰을 읽어와 상태에 저장
  const loadToken = (() => {
    const storedToken = localStorage.getItem('token');
    name.value = localStorage.getItem('name')
    if (storedToken) {
      token.value = storedToken;
      isLoggedIn.value = true;
    }
  })

  const createUserInfo = (payload => {
    const year = payload.targetYear
    const target = payload.targetWealth
    const seed_money = payload.seedMoney
    const invest_aggresive = payload.investAggresive
    const invest_conservative = payload.investConservative
    const salary = payload.salary
    const age = payload.age
    const kor_co_nm = payload.korCoNm
    const industry = payload.industry
    const is_prime_rate = payload.isPrimeRate
    const userToken = token.value
    const data = {
      year, target, seed_money, invest_aggresive, invest_conservative,
      salary, age, kor_co_nm, industry, is_prime_rate, userToken,
    }
    axios({
      method: 'post',
      url: `${API_URL}/portfolio/`,
      data: data
    }).then(res => {
      recommendList.value = res.data.value
      router.push({ name: 'analysis'})
    })
      .catch(err => console.log(err))
  })

  const logout = (() => {
    axios({
        method: 'post',
        url: `${API_URL}/logout/`,
        headers: {
          Authorization: `Token ${token.value}`
      },
    }).then(res => {
        isLoggedIn.value = false
        token.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('name')
    }).catch(err => {
        console.log(err)
    })
})

  const passwordChange = (payload => {
    const password1 = payload.password1
    const password2 = payload.password2
    const data = {
      new_password1: password1,
      new_password2: password2,
    }
    console.log(token.value)
    axios({
      method: 'post',
      url: `${API_URL}/password/change/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: data
    }).then(res => {
      logout()
      router.push({name: 'signIn'})
    }).catch(err => {
      window.alert(err.response.data.new_password2)
      })
  })

  return { API_URL, name, token, isLogin, portfolioId, recommendList, signUp, signIn, createUserInfo, logout, passwordChange, loadToken}
})
