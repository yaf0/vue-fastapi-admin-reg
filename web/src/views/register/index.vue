<template>
  <AppPage :show-footer="true" bg-cover :style="{ backgroundImage: `url(${bgImg})` }">
    <div
      style="transform: translateY(25px)"
      class="m-auto max-w-1500 min-w-345 f-c-c rounded-10 bg-white bg-opacity-60 p-15 card-shadow"
      dark:bg-dark
    >
      <div hidden w-380 px-20 py-35 md:block>
        <icon-custom-front-page pt-10 text-300 color-primary></icon-custom-front-page>
      </div>

      <div w-320 flex-col px-20 py-35>
        <h5 f-c-c text-24 font-normal color="#6a6a6a">
          <icon-custom-logo mr-10 text-50 color-primary />{{ $t('app_name') }}
        </h5>
        <div mt-30>
          <n-input
            v-model:value="registerInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="请输入用户名"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="registerInfo.password"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="请输入密码"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="registerInfo.confirmPassword"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="请确认密码"
            :maxlength="20"
            @keypress.enter="handleRegister"
          />
        </div>

        <div mt-20>
          <n-button
            h-50
            w-full
            rounded-5
            text-16
            type="primary"
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </n-button>
        </div>
        <div mt-20 text-center>
          <router-link to="/login" class="text-primary">已有账号？去登录</router-link>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import bgImg from '@/assets/images/login_bg.webp'
import api from '@/api'

const router = useRouter()
const $message = useMessage()

const registerInfo = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

const loading = ref(false)

async function handleRegister() {
  const { username, password, confirmPassword } = registerInfo.value
  
  if (!username || !password || !confirmPassword) {
    $message.warning('请填写完整信息')
    return
  }

  if (password !== confirmPassword) {
    $message.warning('两次密码输入不一致')
    return
  }

  try {
    loading.value = true
    await api.createUser({
      username,
      password,
      is_active: true,
      is_superuser: false,
      role_ids: [],
      dept_id: null
    })
    $message.success('注册成功')
    router.push('/login')
  } catch (e) {
    console.error('register error', e)
    $message.error(e.message || '注册失败')
  } finally {
    loading.value = false
  }
}
</script> 