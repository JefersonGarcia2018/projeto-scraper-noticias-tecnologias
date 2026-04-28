<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Novo Usuário</div>
    <q-card flat bordered style="max-width: 600px">
      <q-card-section>
        <div class="text-h6">Cadastrar Colaborador ou Administrador</div>
        <q-form @submit="addUser" class="q-gutter-md q-mt-sm">
          <q-input v-model="form.username" label="Nome de Usuário (Login)" outlined dense required />
          <q-input v-model="form.email" label="E-mail Corporativo" outlined dense required type="email" />
          <q-input v-model="form.password" label="Senha Inicial" outlined dense required type="password" />
          <q-select v-model="form.role" :options="['colaborador', 'admin']" label="Nível de Permissão (Cargo)" outlined dense />
          <q-btn label="Cadastrar e Salvar" type="submit" color="indigo" class="full-width" />
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { reactive } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const form = reactive({
  username: '',
  email: '',
  password: '',
  role: 'colaborador'
})

const addUser = async () => {
  try {
    await api.post('/api/v1/users/', form)
    $q.notify({ type: 'positive', message: 'Usuário registrado com sucesso!' })
    form.username = ''
    form.email = ''
    form.password = ''
  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Erro: Usuário/Email podem achar em duplicidade ou você não tem permissão.' })
  }
}
</script>
