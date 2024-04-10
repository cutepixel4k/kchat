<script setup lang="ts">
  import { onMounted, ref } from "vue";
  import type { Message } from "@/api/ktypes";
  import anime from "animejs";

  // { username, self, notify, message: { type, context, reply } }
  const props = defineProps<{ message: Message }>();

  const messageOptionsShow = ref(false);

  // checks and returns reply
  function replyCheck() {
    const data = props.message;

    // -----------------------------------
    if (data.self) {
      // if self user you replied
      if (data.message.reply.username === data.username) {
        // i replied for my own message
        return "You replied yourself";
      } else {
        return "You replied to " + data.message.reply.username;
      }
    } else {
      // if another person replied
      if (data.message.myusername === data.message.reply.username) {
        // if message for self
        return data.username + " replied to you ";
      } else {
        if (data.username === data.message.reply.username) {
          return data.username + " replied themself";
        }

        return data.username + " replied to " + data.message.reply.username;
      }
    }
  }

  function onReplyClick() {}

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
  //
</script>

<template>
  <!-- Bottom  -->

  <div
    @mouseleave="messageOptionsShow = false"
    :id="props.message.msgid"
    class="chat"
    :class="props.message.self ? 'chat-end' : 'chat-start flex flex-col'"
  >
    <!-- reply message -->
    <div
      @click="onReplyClick"
      :class="props.message.self ? 'rounded-bl-lg' : 'rounded-br-lg'"
      class="bg-info text-info-content rounded-t-lg p-1 px-3 mx-3"
    >
      {{ props.message.message.reply.message.content }}
    </div>

    <div @mouseenter="messageOptionsShow = true" class="chat-bubble">
      {{ props.message.message.content }}
    </div>
    <div class="chat-footer">
      {{ replyCheck() }}
    </div>
  </div>
</template>
