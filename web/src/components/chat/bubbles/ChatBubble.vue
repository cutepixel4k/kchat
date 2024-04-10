<script setup lang="ts">
  import ReplyBubble from "./ReplyBubble.vue";
  import TextBubble from "./TextBubble.vue";
  import NotifyBubble from "./NotifyBubble.vue";
  import MessageOptions from "./MessageOptions.vue";
  import type { Message } from "@/api/ktypes";
  import { onMounted, ref } from "vue";
  import anime from "animejs";

  const props = defineProps<{
    message: Message;
    messageOption: any;
    updateScroll: any;
  }>();

  const messageOptionsShow = ref(false);

  function replyMessage(option: string) {
    props.messageOption(option, props.message);
  }

  // double click to show options
  function onDblClick() {
    messageOptionsShow.value = true;
  }

  function isMention() {
    if (
      props.message.message.mentionUsername === props.message.message.myusername
    ) {
      // ------------
      return "animate-bounce";
    } else if (props.message.message.type === "secret") {
      return "animate-pulse";
    }
    return "";
  }

  // TDDO make function optimize
  onMounted(() => {
    props.updateScroll();
    // ---------------------- animate bubble
    var translate = {
      x: [0, 0],
      y: [0, 0],
    };
    if (props.message.notify) {
      translate.y = [100, 0];
      // ------------------------------ notify animation
    } else {
      // ------------------------------ message animation
      translate.x = props.message.self ? [100, 0] : [-100, 0];
    }
    anime({
      targets: document.getElementById(props.message.msgid),
      translateX: translate.x,
      translateY: translate.y,
    });
  });
</script>

<template>
  <!-- notify in middle -->
  <NotifyBubble v-if="props.message.notify" :notify="props.message" />

  <!-- message bubble -->
  <div
    :class="isMention()"
    class="rounded-lg font-medium"
    v-else
    @dblclick="onDblClick"
    @mouseleave="messageOptionsShow = false"
  >
    <!-- <ReplyBubble /> -->
    <ReplyBubble v-if="props.message.message.reply" :message="props.message" />
    <TextBubble v-else :message="props.message" />
    <!-- message options -->
    <div
      class="absolute bottom-12"
      :class="props.message.self ? 'right-0' : 'left-0'"
      v-if="messageOptionsShow"
    >
      <MessageOptions
        :messageOption="replyMessage"
        :showUnsend="props.message.self"
      />
    </div>
  </div>
</template>

<style>
  .mention {
    background-color: rgba(0, 0, 40, 0.3);
  }
  .secret {
    background-color: rgba(0, 30, 0, 0.3);
  }
</style>
