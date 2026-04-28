<template>
  <q-page class="q-pa-md">
    <div class="text-h5 q-mb-md">Visão Geral</div>
    <q-card flat bordered class="bg-grey-2">
      <q-card-section>
        <div class="text-h6">Conta Conectada</div>
        <p class="q-mt-sm">Você está autenticado como <strong>{{ userStore.user }}</strong>.</p>
        <q-chip color="indigo" text-color="white" icon="badge" :label="'Acesso: ' + (userStore.isAdmin ? 'Administrador' : 'Colaborador')" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { useUserStore } from 'stores/userStore'
const userStore = useUserStore()
</script>
