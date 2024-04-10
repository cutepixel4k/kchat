<script setup lang="ts">
  const props = defineProps<{
    title: string;
    desc: string;
    onClick: any;
  }>();
</script>

<template>
  <div class="w-full h-full flex gap-2 justify-center items-center p-2">
    <!-- pop up -->
    <div
      class="p-5 flex flex-col items-center justify-center gap-3 ring-2 rounded-lg"
    >
      <h1>Do you want to remove user</h1>
      <div class="space-x-2">
        <button class="btn btn-error btn-sm" @click="props.onClick('Yes')">
          No
        </button>
        <button class="btn btn-success btn-sm" @click="props.onClick('No')">
          Yes
        </button>
      </div>
    </div>
  </div>
</template>
