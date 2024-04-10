<script setup lang="ts">
  import Navbar from "@/components/Navbar.vue";
  import Rooms from "@/components/Rooms.vue";
</script>

<template>
  <main class="h-screen flex flex-col overflow-hidden">
    <!-- navbar -->
    <Navbar title="KCHAT" />
    <!-- chat -->
    <Rooms />
  </main>
</template>
