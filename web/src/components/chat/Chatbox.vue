<script setup lang="ts">
  import { onBeforeMount, onMounted, onUpdated, ref } from "vue";
  import ChatBubble from "./bubbles/ChatBubble.vue";

  import type { Message } from "@/api/ktypes";
  // import { useRoomStore } from "@/stores/room";

  // const props = defineProps<{ message: Message }>();

  // const roomStore = useRoomStore();
  const clearTimer = ref(0);

  //   message
  const messages = ref<Message[]>([]);

  const chatbox = ref<Element>();
  const props = defineProps(["replyMessage"]);

  function updateScroll() {
    if (chatbox.value) {
      chatbox.value.scrollTop = chatbox.value.scrollHeight;
    }
  }

  function addMessage(message: Message) {
    console.log("GOT (ADD MESSAGE): ", message);

    messages.value.push(message);
  }

  function specialMessage() {}

  function unsendMessage(msgID: string, userName: string) {
    const i = messages.value.findIndex(
      (v) => v.username === userName && v.msgid === msgID
    );

    if (i >= 0) {
      messages.value.splice(i, 1);
    }
  }

  defineExpose({ addMessage, unsendMessage, specialMessage });

  // entry for replying for all message options
  function messageOption(option: string, v: Message) {
    props.replyMessage(option, v);
  }

  function onOneSecond() {
    const value = clearTimer.value;

    if (value === 60) {
      // clear all messages
      messages.value = [];
      clearTimer.value = 0;
    } else {
      clearTimer.value += 1;
    }
  }

  function startAutoRemove() {
    setInterval(() => {
      onOneSecond();
    }, 1000);

    window.onblur = () => {
      messages.value = [];
    };

    updateScroll();
  }

  onMounted(() => {
    // startAutoRemove()
  });
</script>

<template>
  <div
    id="chatbox"
    ref="chatbox"
    class="h-full overflow-y-auto overflow-x-hidden p-2 select-none flex flex-col"
  >
    <!-- emply div that srinks -->
    <div class="flex-1 md:flex-none"></div>
    <div :id="message.msgid" v-for="(message, i) in messages" :key="i">
      <ChatBubble :message :messageOption="messageOption" :updateScroll />
    </div>
  </div>
</template>
