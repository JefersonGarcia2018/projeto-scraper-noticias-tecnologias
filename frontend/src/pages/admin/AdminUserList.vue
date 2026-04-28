<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Gestão de Equipe</div>
    
    <q-table
      title="Usuários Cadastrados"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :loading="loading"
      flat bordered
    >
      <template v-slot:body-cell-role="props">
        <q-td :props="props">
          <q-chip
            :color="props.row.role === 'admin' ? 'red' : 'blue'"
            text-color="white"
            dense
          >
            {{ props.row.role.toUpperCase() }}
          </q-chip>
        </q-td>
      </template>

      <template v-slot:body-cell-is_active="props">
        <q-td :props="props">
          <q-icon :name="props.row.is_active ? 'check_circle' : 'cancel'" :color="props.row.is_active ? 'green' : 'grey'" size="sm" />
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const rows = ref([])
const loading = ref(false)

const columns = [
  { name: 'id', required: true, label: 'ID', align: 'left', field: 'id', sortable: true },
  { name: 'username', required: true, label: 'Identificador do Usuário', align: 'left', field: 'username', sortable: true },
  { name: 'email', required: true, label: 'Conta de E-mail', align: 'left', field: 'email', sortable: true },
  { name: 'role', required: true, label: 'Permissão Sistêmica', align: 'center', field: 'role', sortable: true },
  { name: 'is_active', required: true, label: 'Ativo', align: 'center', field: 'is_active', sortable: true }
]

const loadUsers = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/v1/users/')
    rows.value = res.data
  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Erro ao buscar listagem de usuários.' })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>
