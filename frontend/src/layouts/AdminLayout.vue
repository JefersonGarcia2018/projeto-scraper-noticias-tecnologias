<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-indigo-9 text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Painel Administrativo
        </q-toolbar-title>

        <q-btn flat dense icon="home" label="Voltar ao Site" to="/" />
        <q-separator vertical dark inset class="q-mx-sm" />
        <q-btn flat dense icon="logout" label="Sair" @click="logout" />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-1"
    >
      <q-list>
        <q-item-label header>Menu Principal</q-item-label>

        <q-item clickable v-ripple exact to="/admin">
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>
            Início
          </q-item-section>
        </q-item>

        <q-item clickable v-ripple exact to="/admin/scraper">
          <q-item-section avatar>
            <q-icon name="autorenew" />
          </q-item-section>
          <q-item-section>
            Acionar Scraper
          </q-item-section>
        </q-item>

        <q-separator v-if="userStore.isAdmin" class="q-my-sm" />

        <q-expansion-item
          v-if="userStore.isAdmin"
          icon="people"
          label="Usuários"
          default-opened
        >
          <q-item clickable v-ripple exact to="/admin/users/create" class="q-pl-xl">
            <q-item-section avatar>
              <q-icon name="person_add" />
            </q-item-section>
            <q-item-section>
              Cadastrar Usuário
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple exact to="/admin/users/list" class="q-pl-xl">
            <q-item-section avatar>
              <q-icon name="list_alt" />
            </q-item-section>
            <q-item-section>
              Listar Usuários
            </q-item-section>
          </q-item>
        </q-expansion-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from 'stores/userStore'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

const userStore = useUserStore()
const router = useRouter()
const leftDrawerOpen = ref(false)

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const logout = () => {
  userStore.logout()
  delete api.defaults.headers.common['Authorization']
  router.push('/')
}
</script>
