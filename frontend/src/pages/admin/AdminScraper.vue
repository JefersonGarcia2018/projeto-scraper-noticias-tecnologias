<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Acionar Scraper Manual</div>
    <q-card class="q-mb-lg bg-red-1" flat bordered>
      <q-card-section>
        <div class="text-h6 text-red-9">Web Scraper de Notícias Tech</div>
        <p>Ao acionar o botão abaixo, os motores irão vasculhar as notícias e todos os clientes conectados receberão uma notificação instantânea se contiver notícias inéditas.</p>
        <q-btn color="red-9" icon="refresh" label="Iniciar Scraper Agora" @click="runScraper" :loading="scraping" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const scraping = ref(false)

const runScraper = async () => {
  scraping.value = true
  try {
    await api.post('/api/v1/news/scrape')
    $q.notify({ type: 'positive', message: 'Scraper rodando no servidor em formato de Background Task!' })
  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Erro ao rodar scraper.' })
  } finally {
    scraping.value = false
  }
}
</script>
