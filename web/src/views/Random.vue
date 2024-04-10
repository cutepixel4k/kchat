<script setup lang="ts">
  // import Chat from "@/components/chat/Chat.vue";
  import JoinClient from "@/components/chat/JoinClient.vue";
  import Navbar from "@/components/Navbar.vue";
</script>
<template>
  <main class="h-screen flex flex-col overflow-hidden">
    <!-- navbar -->
    <Navbar title="KCHAT RANDOM" />
    <!-- chat -->
    <JoinClient class="flex-1" />
  </main>
</template>
