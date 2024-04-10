<script setup lang="ts">
  import { useRoomStore } from "@/stores/room";
  import ReplyChat from "./bubbles/ReplyChat.vue";
  import { onBeforeUnmount, onMounted, ref } from "vue";
  import Mention from "./input/Mention.vue";

  const roomStore = useRoomStore();
  const mention = ref();

  const input = ref("");
  const showMention = ref(false);

  // const mentionPerson = ref()

  const props = defineProps(["send"]);
  // const inputRef = ref();

  // checking for empty space or inpropriate messages
  function checkEmptySpace() {
    if (input.value.trim().length === 0) {
      input.value = "";
      return true;
    }
  }

  function sendMessage() {
    // props.mentionPerson("kikku", "hi");
    if (checkEmptySpace()) {
      return;
    }
    document.getElementById("kchat-message-input")?.focus();
    props.send(input.value);
    input.value = "";
  }

  function closeReply() {
    roomStore.replyMessage = undefined;
  }

  function onUserSelect(username: string, action: number) {
    if (action === 0) {
      input.value = `@${username} `;
    } else if (action === 1) {
      input.value = `$${username} `;
    }

    //
    document.getElementById("kchat-message-input")?.focus();
    showMention.value = false;
  }
  // ------------ called on every word TODO: optimize
  function onTyping() {
    const value = input.value;

    if (value[0] !== "@" && value[0] !== "$") {
      showMention.value = false;

      return;
    }

    if (value[0] === "@" || value[0] === "$") {
      if (value.split(" ").length === 1) {
        showMention.value = true;
        if (mention.value) {
          mention.value.change(value.slice(1));
        }
      } else {
        showMention.value = false;
      }
      // ----------------
    }
  }

  // window.addEventListener("resize", () => {
  //   alert("hi");
  // });
</script>

<template>
  <div
    class="w-full fixed bottom-0 flex flex-col items-center pb-4 px-2 bg-base-100"
  >
    <!-- reply chat -->
    <ReplyChat
      v-if="roomStore.replyMessage !== undefined"
      :self="roomStore.replyMessage.self"
      :username="roomStore.replyMessage.username"
      :message="roomStore.replyMessage.message"
      :closeReply="closeReply"
    />

    <!-- mention bar -->
    <Mention
      ref="mention"
      v-if="showMention"
      :roomID="roomStore.roomID"
      :onUserSelect
      :username="roomStore.username"
    />

    <!-- frame -->
    <div
      class="w-full border-2 border-neutral rounded-md p-2 px-4 flex justify-between gap-2 items-center"
    >
      <!-- left icons -->
      <div
        @click="showMention = !showMention"
        class="w-3 text-error hover:cursor-pointer"
      >
        <span>😎</span>
      </div>
      <!-- input -->
      <div class="flex-1">
        <input
          id="kchat-message-input"
          v-model="input"
          ref="inputRef"
          autofocus="true"
          autocomplete="off"
          @keyup.enter="sendMessage"
          @keyup="onTyping"
          type="search"
          placeholder="Type Here..."
          class="w-full px-2 h-full bg-base-100 focus:outline-none placeholder:text-base-context"
        />
      </div>
      <!-- right icons -->
      <div>
        <!-- buttons 1 ( only on typing ) -->
        <div class="flex gap-2">
          <button @click="sendMessage" class="text-primary">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  #Search::-webkit-search-cancel-button {
    visibility: hidden;
  }
</style>
