<script setup lang="ts">
  // import type { Message } from "@/api/ktypes";
  // import { useRoomStore } from "@/stores/room";
  import anime from "animejs";
  import { onMounted } from "vue";

  const props = defineProps<{ messageOption: any; showUnsend: boolean }>();

  onMounted(() => {
    anime({
      targets: document.getElementById("msgoptions"),
      translateY: [-20, 0],
    });

    const chatbox = document.getElementById("chatbox");

    if (chatbox) {
      chatbox.scrollTop = chatbox.scrollHeight;
    }
  });
</script>

<template>
  <div
    id="msgoptions"
    class="bg-secondary p-2 text-secondary-content rounded-md flex gap-3 items-center z-50"
  >
    <button @click="props.messageOption('reply')">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="22"
        height="22"
        fill="currentColor"
        class="bi bi-reply"
        viewBox="0 0 16 16"
      >
        <path
          d="M6.598 5.013a.144.144 0 0 1 .202.134V6.3a.5.5 0 0 0 .5.5c.667 0 2.013.005 3.3.822.984.624 1.99 1.76 2.595 3.876-1.02-.983-2.185-1.516-3.205-1.799a8.7 8.7 0 0 0-1.921-.306 7 7 0 0 0-.798.008h-.013l-.005.001h-.001L7.3 9.9l-.05-.498a.5.5 0 0 0-.45.498v1.153c0 .108-.11.176-.202.134L2.614 8.254l-.042-.028a.147.147 0 0 1 0-.252l.042-.028zM7.8 10.386q.103 0 .223.006c.434.02 1.034.086 1.7.271 1.326.368 2.896 1.202 3.94 3.08a.5.5 0 0 0 .933-.305c-.464-3.71-1.886-5.662-3.46-6.66-1.245-.79-2.527-.942-3.336-.971v-.66a1.144 1.144 0 0 0-1.767-.96l-3.994 2.94a1.147 1.147 0 0 0 0 1.946l3.994 2.94a1.144 1.144 0 0 0 1.767-.96z"
        />
      </svg>
    </button>
    <!-- divider -->
    <div v-if="props.showUnsend" class="border h-4 bg-gray-200"></div>
    <!-- unsend -->
    <button v-if="props.showUnsend" @click="props.messageOption('unsend')">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="18"
        height="18"
        fill="currentColor"
        class="bi bi-trash"
        viewBox="0 0 16 16"
      >
        <path
          d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"
        />
        <path
          d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"
        />
      </svg>
    </button>
  </div>
</template>
