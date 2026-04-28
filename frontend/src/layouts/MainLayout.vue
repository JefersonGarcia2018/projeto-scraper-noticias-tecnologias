<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-red-9 text-white">
      <q-toolbar>
        <q-toolbar-title>
          Portal Notícias Tech
        </q-toolbar-title>

        <q-btn flat dense icon="home" label="Home" to="/" />
        
        <q-separator vertical dark inset class="q-mx-sm" />

        <template v-if="userStore.isAuthenticated">
          <q-btn flat dense icon="admin_panel_settings" label="Painel" to="/admin" />
          <q-btn flat dense icon="logout" label="Sair" @click="logout" />
        </template>
        <template v-else>
          <q-btn flat dense icon="login" label="Logar" to="/login" />
        </template>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useUserStore } from 'stores/userStore'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  delete api.defaults.headers.common['Authorization']
  router.push('/')
}
</script>
