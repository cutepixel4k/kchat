<script setup lang="ts">
  import { ref } from "vue";

  const props = defineProps(["login"]);

  const input = ref("");

  function loginAdmin() {
    if (input.value.length > 0) {
      props.login(input.value);
      input.value = "";
    }
  }
</script>

<template>
  <div class="w-full h-full flex flex-col justify-center items-center gap-2">
    <input
      v-model="input"
      type="text"
      class="input h-10 border-2 border-secondary"
      placeholder="Admin Key"
    />
    <button @click="loginAdmin" class="btn btn-sm btn-outline">LOGIN</button>
  </div>
</template>
