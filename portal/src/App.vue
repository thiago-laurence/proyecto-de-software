<script setup>
  import { RouterView } from 'vue-router'
  import Header from './components/Header.vue'
</script>

<template>
    <Header></Header>
    <main class="mt-20 ">
      <!-- Contenido principal de la página -->
      <RouterView />
    </main>
</template>





