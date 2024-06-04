import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/authentication/SignUpView.vue'
import SignInView from '@/views/authentication/SignInView.vue'
import PasswordChangeView from '@/views/authentication/PasswordChangeView.vue'
import InputUserInfoView from '@/views/InputUserInfoView.vue'
import MypageView from '@/views/MyPageView.vue'
import AnalysisView from '@/views/AnalysisView.vue'
import CorporationDetailView from '@/views/CorporationDetailView.vue'
import StockListView from '@/views/StockListView.vue'
import DepositListView from '@/views/DepositListView.vue'
import SavingListView from '@/views/SavingListView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signUp',
      component: SignUpView,
    },
    {
      path: '/signin',
      name: 'signIn',
      component: SignInView,
    },
    {
      path: '/password/change',
      name: 'passwordChange',
      component: PasswordChangeView,
    },
    {
      path: '/profile/:userId',
      name: 'myPage',
      component: MypageView,
    },
    {
      path: '/analysis',
      name: 'inputUserInfo',
      component: InputUserInfoView,
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: AnalysisView,
    },
    {
      path: '/stock',
      name: 'stock',
      component: StockListView
    },
    {
      path: '/deposit',
      name: 'deposit',
      component: DepositListView,
    },
    {
      path: '/saving',
      name: 'saving',
      component: SavingListView
    },
    {
      path: '/:coperationname/detail',
      name: 'coperation',
      component: CorporationDetailView
    },
  ]
})

// 이거 문제는 url의 직접 수정을 막지 못 함
// router.beforeEach((to, from) => {
//   const store = useUserStore()
//   console.log(to)
//   // 로그인이 되어 있을 때, 로그인이나 회원가입 뷰에 접근하려고 시도하는 경우
//   if (to.name === 'signUp' || to.name === 'signIn' && (store.isLogin)) {
//     window.alert('이미 로그인이 되어 있습니다.')
//     return {name: from.name }
//   }
// })
export default router
