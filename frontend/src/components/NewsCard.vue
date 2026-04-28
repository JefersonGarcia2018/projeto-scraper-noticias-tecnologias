<template>
  <q-card class="news-card q-mb-md flat bordered" clickable @click="openLink">
    <div class="row no-wrap">
      <q-img
        v-if="news.image_url"
        :src="news.image_url"
        class="col-4"
        style="min-height: 120px; border-radius: 8px 0 0 8px;"
        fit="cover"
      />
      <q-card-section class="col-8 column justify-between">
        <div>
          <div class="text-h6 text-red-9 text-weight-bold" style="line-height: 1.2;">
            {{ news.title }}
          </div>
          <div class="text-subtitle2 text-grey-8 q-mt-sm" v-if="news.summary" style="line-height: 1.4;">
            {{ news.summary }}
          </div>
        </div>
        <div class="text-caption text-grey-6 q-mt-md row items-center justify-between">
          <span>{{ news.published_date || 'Data desconhecida' }} — Em Tecnologia</span>
          <q-btn v-if="userStore.isAdmin" @click.stop="triggerDelete" dense flat round icon="delete" color="red" title="Excluir Notícia (Apenas Admin)" />
        </div>
      </q-card-section>
    </div>
  </q-card>
</template>

<script setup>
import { useUserStore } from 'stores/userStore'

const userStore = useUserStore()
const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['deleted'])

const triggerDelete = () => {
  emit('deleted', props.news.id)
}

const openLink = () => {
  window.open(props.news.link, '_blank')
}
</script>

<style scoped>
.news-card {
  border-radius: 8px;
  transition: box-shadow 0.2s ease-in-out;
  cursor: pointer;
}
.news-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
