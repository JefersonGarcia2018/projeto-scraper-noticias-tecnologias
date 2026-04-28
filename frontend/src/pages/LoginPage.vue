<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card class="q-pa-md shadow-2 my_card" style="width: 400px">
      <q-card-section class="text-center">
        <div class="text-h5 text-weight-bold text-red-9">Login Interno</div>
        <div class="text-subtitle2 text-grey-6">Área para Colaboradores e Administradores</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <q-input v-model="form.username" label="E-mail Corporativo" type="email" outlined />
          <q-input v-model="form.password" type="password" label="Senha" outlined />
          <div>
            <q-btn label="Login" type="submit" color="red-9" class="full-width" />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { reactive } from 'vue'
import { useUserStore } from 'stores/userStore'
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const router = useRouter()
const userStore = useUserStore()
const $q = useQuasar()

const form = reactive({
  username: '',
  password: ''
})

const onSubmit = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', form.username)
    formData.append('password', form.password)

    const res = await api.post('/api/v1/auth/login', formData)
    
    // Save token and fetch user data logic
    const token = res.data.access_token
    userStore.setToken(token)
    
    // Decode token to get role
    const payload = JSON.parse(atob(token.split('.')[1]))
    userStore.roles = [payload.role]
    userStore.user = payload.sub
    
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
    $q.notify({ type: 'positive', message: 'Bem-vindo(a)!' })
    router.push('/admin')
  } catch (error) {
    if (error.response && error.response.status === 401) {
      $q.notify({ type: 'negative', message: 'Credenciais inválidas.' })
    } else {
      $q.notify({ type: 'negative', message: 'Erro no servidor.' })
    }
  }
}
</script>
