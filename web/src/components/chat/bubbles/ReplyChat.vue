<script setup lang="ts">
  import { useRoomStore } from "@/stores/room";
  import anime from "animejs";
  import { onMounted } from "vue";

  // const roomStore = useRoomStore();
  const props = defineProps(["self", "username", "message", "closeReply"]);

  onMounted(() => {
    anime({
      targets: ".reply-bar",
      translateX: [-100, 0],
    });
  });
</script>

<template>
  <div
    class="w-full skeleton rounded-none bg-base-200 relative text-base-content reply-bar -z-50 ring-2 ring-secondary/60"
  >
    <!-- reply -->
    <div class="w-full px-12">
      <!-- reply -->
      <h1 class="font-bold">
        Replying to
        {{ props.self ? "Yourself" : props.username }}
      </h1>
      <p class="truncate">{{ props.message.content }}</p>
    </div>
    <!-- close button -->
    <!-- @click="roomStore.replyMessage = undefined" -->
    <div
      class="absolute top-3 right-5 hover:cursor-pointer"
      @click="props.closeReply"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="25"
        height="25"
        fill="currentColor"
        class="bi bi-x-lg"
        viewBox="0 0 16 16"
      >
        <path
          d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"
        />
      </svg>
    </div>
  </div>
</template>
