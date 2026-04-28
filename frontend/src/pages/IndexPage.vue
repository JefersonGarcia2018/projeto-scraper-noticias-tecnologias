<template>
  <q-page class="q-pa-md flex flex-center bg-grey-2">
    <div style="max-width: 800px; width: 100%;">
      <div class="row items-center justify-between q-mb-lg">
        <div class="text-h4 text-weight-bolder text-red-9">Notícias Tech</div>
        <q-btn v-if="isConnected" flat round color="green" disable icon="wifi" aria-label="WS Online" />
        <q-btn v-else flat round color="grey" disable icon="wifi_off" aria-label="WS Offline" />
      </div>

      <div v-if="loading" class="text-center q-my-xl">
        <q-spinner-dots color="red-9" size="40px" />
      </div>
      
      <div v-else-if="newsList.length === 0" class="text-center text-h6 text-grey-6 q-my-xl">
        Nenhuma notícia cadastrada no momento.
      </div>

      <div v-else>
        <NewsCard v-for="item in newsList" :key="item.id" :news="item" @deleted="handleDelete" />
        
        <div class="q-mt-lg flex flex-center">
          <q-btn v-if="newsList.length >= 50" outline color="red-9" label="Mostrar mais" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from 'boot/axios'
import NewsCard from 'components/NewsCard.vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const newsList = ref([])
const loading = ref(true)
const isConnected = ref(false)
let ws = null

const fetchNews = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/v1/news/')
    newsList.value = res.data
  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Erro ao carregar notícias.' })
  } finally {
    loading.value = false
  }
}

const handleDelete = async (newsId) => {
  $q.dialog({
    title: 'Excluir Notícia',
    message: 'Tem certeza que deseja apagar permanentemente essa notícia do seu site?',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await api.delete(`/api/v1/news/${newsId}`)
      newsList.value = newsList.value.filter(n => n.id !== newsId)
      $q.notify({ type: 'positive', message: 'Notícia excluída.' })
    } catch (error) {
      console.error(error)
      $q.notify({ type: 'negative', message: 'Falha ao excluir notícia (Permissão negada ou Backend offline).' })
    }
  })
}

const setupWebSocket = () => {
  ws = new WebSocket('ws://localhost:8000/ws/news')
  ws.onopen = () => {
    isConnected.value = true
  }
  ws.onmessage = (event) => {
    $q.notify({
      color: 'red-9',
      textColor: 'white',
      icon: 'update',
      message: event.data,
      actions: [{ label: 'Atualizar', color: 'white', handler: () => fetchNews() }]
    })
  }
  ws.onclose = () => {
    isConnected.value = false
    setTimeout(setupWebSocket, 3000) // Reconnect try
  }
}

onMounted(() => {
  fetchNews()
  setupWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})
</script>
