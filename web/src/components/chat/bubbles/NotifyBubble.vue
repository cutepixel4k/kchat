<script setup lang="ts">
  import type { Message } from "@/api/ktypes";
  const props = defineProps<{ notify: Message }>();
</script>

<template>
  <div class="w-full flex justify-between items-center gap-3 opacity-80">
    <div class="border-t-2 flex-1 border-info mt-1"></div>
    <h1 class="flex gap-2">
      <p class="text-primary">{{ props.notify.username }}</p>
      <p class="text-secondary">{{ props.notify.message }}</p>
    </h1>
    <div class="border-t-2 flex-1 border-info mt-1"></div>
  </div>
</template>

<style>
  .v-enter-active,
  .v-leave-active {
    transition: opacity 0.5s ease;
  }

  .v-enter-from,
  .v-leave-to {
    opacity: 0;
  }
</style>
