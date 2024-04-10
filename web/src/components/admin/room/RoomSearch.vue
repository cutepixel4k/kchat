<script setup lang="ts">
  import { ref } from "vue";

  const props = defineProps<{ getDetails: any }>();
  const roomID = ref();
</script>

<template>
  <div class="flex items-center p-2 gap-3">
    <input
      v-model="roomID"
      type="search"
      class="w-full p-1 outline-none rounded-lg bg-base-100 ring-1"
      placeholder="Room name or Room ID"
    />
    <button @click="props.getDetails(roomID)">SEARCH</button>
  </div>
</template>
