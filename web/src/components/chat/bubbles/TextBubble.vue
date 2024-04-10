<script setup lang="ts">
  import anime from "animejs";
  import { onMounted, ref } from "vue";
  import type { Message } from "@/api/ktypes";

  const props = defineProps<{ message: Message }>();
  const messageOptionsShow = ref(false);

  onMounted(() => {
    // var translateX = [-100, 0];
    // if (props.message.self) {
    //   translateX = [100, 0];
    // }
    // anime({
    //   targets: document.getElementById(props.message.msgid),
    //   translateX: translateX,
    // });
  });

  function hideOptions() {
    // -----------------------
    messageOptionsShow.value = false;
  }
</script>

<template>
  <div
    @mouseleave="hideOptions"
    class="chat"
    :class="props.message.self ? 'chat-end' : 'chat-start'"
  >
    <!-- only rendered on user messages -->
    <div class="chat-header" v-if="!props.message.self">
      {{ props.message.username }}
    </div>
    <div
      @mouseenter="messageOptionsShow = true"
      class="chat-bubble"
      :class="
        props.message.self ? 'chat-bubble-primary text-primary-content' : ''
      "
    >
      {{ props.message.message.content }}
    </div>
  </div>
</template>
