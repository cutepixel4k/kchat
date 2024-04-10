<script setup lang="ts">
  import type { Setting } from "@/api/ktypes";
  import { ref } from "vue";

  const props = defineProps<{ setting: Setting }>();
  const value = ref(props.setting.value);
</script>

<template>
  <div class="w-full">
    <div class="flex gap-2 py-1">
      <h1
        class="font-semibold uppercase text-info w-full text-center lg:text-left"
      >
        {{ props.setting.label }}
      </h1>
    </div>
    <!-- text area -->
    <textarea
      v-if="props.setting.tp === 'textarea'"
      :name="props.setting.key"
      :class="props.setting.tp"
      :placeholder="props.setting.hint"
      class="w-full h-24"
      cols="30"
      v-model="value"
    ></textarea>
    <!-- choice -->

    <!-- input text | number -->
    <input
      v-else
      :name="props.setting.key"
      class="my-input"
      :class="props.setting.tp"
      :placeholder="props.setting.hint"
      :type="props.setting.tp"
      v-model="value"
    />
    <!-- description -->
    <p class="text-base-context">{{ props.setting.desc }}</p>
  </div>
</template>

<style scoped>
  .my-input {
    @apply text-base-content placeholder:px-1 w-full p-2 lg:p-1 border-2 border-secondary rounded-lg bg-base-100 px-4 focus:outline-none;
  }
  .textarea {
    @apply ring-2;
  }
</style>
