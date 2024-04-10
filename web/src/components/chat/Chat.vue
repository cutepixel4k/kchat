<script setup lang="ts">
  import Loading from "./sub/Loading.vue";
  import Chatbox from "./Chatbox.vue";
  import Input from "./Input.vue";

  import { onMounted, onUnmounted, ref } from "vue";
  import { backendURL, createConnection, joinConnection } from "@/api/socket";

  import { useRoomStore } from "@/stores/room";
  // types
  import type {
    JoinUserInterface,
    Message,
    createUserInterface,
  } from "@/api/ktypes";

  const props = defineProps<{
    create: createUserInterface | undefined;
    join: JoinUserInterface | undefined;
    onSuccess: any;
    onClose: any;
  }>();

  const chatbox = ref();

  const roomStore = useRoomStore(); // stores room info
  // const roomUsername = ref<string>();
  const roomDetails = ref<{
    roomUsername: string; // update from to this
    roomName: string;
    roomID: string;
    roomLimit: string;
    roomDescription: string;
  }>();

  // used to show loading screen
  const state = ref({
    login: true,
    loading: false,
    open: false,
  });
  var socket: undefined | WebSocket = undefined;

  // on message from backend
  function onSocketMessage(e: any) {
    const data = JSON.parse(e.data);

    const cmd = data.cmd;
    const values = data.values;

    const msgself =
      values.username === roomDetails.value?.roomUsername ? true : false;

    // creating message object
    const message: Message = {
      username: values.username,
      message: values.message,
      self: msgself,
      notify: false,
      msgid: values.msgid,
    };

    if (cmd === "message") {
      values.message.myusername = roomStore.username;
      chatbox.value.addMessage(message);
    }
    // -------------------------- unsend
    else if (cmd === "msg-unsend") {
      // -----------------------
      chatbox.value.unsendMessage(values.msgid, values.username);
    }
    // --------------------- mention
    else if (cmd === "msg-mention") {
      message.message.myusername = roomStore.username;
      // ------------------------------ message with mention
      chatbox.value.addMessage(message);
    }
    // emited when notify message
    else if (cmd === "notify") {
      if (roomDetails.value) {
        roomDetails.value.roomLimit = values.room_limit;
      }
      message.notify = true;

      chatbox.value.addMessage(message);
    }
    // on connected ------------ success
    else if (cmd === "success") {
      roomDetails.value = {
        roomUsername: values.userName,
        roomID: values.roomID,
        roomName: values.roomName,
        roomLimit: values.room_limit,
        roomDescription: values.roomDescription,
      };
      roomStore.roomID = values.roomID;
      // calling success connection
      props.onSuccess();
      // ---------------------------------
      roomStore.inRoom = true;
      roomStore.username = values.userName;
      // success settings
      state.value.open = true;
      state.value.loading = false;
    } else {
    }
  }

  function onSocketConnect(e: any) {}

  function onSocketDisconnect(e: CloseEvent) {
    roomStore.inRoom = false;
    roomStore.replyMessage = undefined;
    props.onClose(e.reason);
  }

  // connect and bind callbacks
  function bindSocket(URL: string) {
    socket = new WebSocket(URL);

    socket.onmessage = onSocketMessage;
    socket.onopen = onSocketConnect;
    socket.onclose = onSocketDisconnect;
  }

  async function createUser(user: createUserInterface) {
    state.value.loading = true;
    state.value.login = false;

    const URL = createConnection(
      user.username,
      user.roomName,
      user.password,
      user.isPublic
    );
    bindSocket(URL);

    // set them in success message
    roomStore.roomID = roomDetails.value?.roomID;
    roomStore.username = user.username;
  }

  async function joinUser(user: JoinUserInterface) {
    state.value.loading = true;
    state.value.login = false;
    const URL = joinConnection(user.username, user.roomID, user.password);
    bindSocket(URL);
  }

  // send message to server
  function sendFromInput(value: string) {
    var data;
    // if connection not open
    if (state.value.open === false) return;
    if (chatbox.value === undefined || socket === undefined) return;
    // if chat box ref found

    data = {
      type: "message",
      content: value,
      reply: roomStore.replyMessage,
      mentionUsername: "",
    };

    // if message mention or private message
    if (value.startsWith("@")) {
      const username = value.split(" ")[0].slice(1);
      data.mentionUsername = username;
      // ---------------------------------
    } else if (value.startsWith("$")) {
      // ------------------------------- send secret message
      const username = value.split(" ")[0].slice(1);
      data = {
        type: "secret",
        content: value,
        reply: roomStore.replyMessage,
        // ---------------------------
        secret_username: username,
      };
    }
    roomStore.replyMessage = undefined;
    // sending message to socket
    socket.send(JSON.stringify(data));
  }

  // send this to chatbox to reply for message
  function replyMessage(option: string, v: Message) {
    // reply message
    if (option === "reply") {
      roomStore.replyMessage = v;

      // focus user input box
      document.getElementById("kchat-message-input")?.focus();
    }
    // remove message
    else if (option === "unsend") {
      if (socket === undefined) return;

      socket.send(
        JSON.stringify({
          // ----------------------------- send to backend
          type: "msg-unsend",
          msgid: v.msgid,
        })
      );
    }
  }

  function shareLink() {
    if (navigator.share) {
      navigator.share({
        title: "KCHAT JOIN ROOM",
        url:
          `${location.protocol}//${location.host}/room/join?roomID=` +
          roomDetails.value?.roomID,
      });
    }
  }

  function copyLink() {
    const copyText =
      `${location.protocol}//${location.host}/room/join?roomID=` +
      roomDetails.value?.roomID;
    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText);
  }

  onMounted(() => {
    if (props.join) {
      // ------------------------- join user
      joinUser(props.join);
    } else if (props.create) {
      // ------------------------- create user
      createUser(props.create);
    }
  });

  onUnmounted(() => {
    console.log("chat unmounted");
  });
</script>

<template>
  <div class="w-full h-full relative">
    <Loading v-if="state.loading" />
    <!-- <JoinChat v-if="state.login" :joinUser :createUser :close /> -->
    <!-- chat messages -->
    <div v-else class="w-full h-full flex flex-col overflow-hidden">
      <!-- small navbar -->
      <div
        class="p-2 mt-1 border-2 rounded-lg text-base-content opacity-80 flex justify-between items-center truncate"
      >
        <!-- title -->
        <div class="flex gap-3 items-center">
          <a href="/">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              fill="currentColor"
              class="bi bi-arrow-left"
              viewBox="0 0 16 16"
            >
              <path
                fill-rule="evenodd"
                d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"
              />
            </svg>
          </a>

          <h1>{{ roomDetails?.roomLimit }}</h1>
        </div>

        <div class="flex gap-2">
          <!-- members -->

          <!-- share -->
          <div class="flex gap-2 font-semibold">
            <button
              @click="shareLink"
              class="btn btn-info btn-sm text-info-content"
            >
              SHARE
            </button>
            <!-- copy -->

            <div class="tooltip tooltip-left" data-tip="copied">
              <button
                @click="copyLink"
                class="btn btn-accent btn-sm text-accent-content"
              >
                COPY
              </button>
            </div>
          </div>
        </div>
        <!-- share -->
      </div>

      <!-- chatbox -->
      <Chatbox ref="chatbox" class="flex-1" :replyMessage />

      <!-- room description -->
      <div
        id="room-info"
        class="h-32 overflow-y-hidden flex flex-col items-center text-base-content p-2 text-center opacity-60"
      >
        <div
          class="border-2 w-full md:w-1/2 md:h-full rounded-lg border-base-content"
        >
          <h1>{{ roomDetails?.roomName }}</h1>
          <h1>{{ roomDetails?.roomDescription }}</h1>
        </div>
      </div>
      <!-- reply to -->

      <!-- input -->
      <Input v-if="roomStore.inRoom" :send="sendFromInput" />
    </div>
  </div>
</template>
