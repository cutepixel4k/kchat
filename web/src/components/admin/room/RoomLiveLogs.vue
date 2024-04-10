<script setup lang="ts">
  import { getAdminCookie } from "@/api/admin";
  import { adminSocketURL, backendURL } from "@/api/socket";
  import axios from "axios";
  import { onMounted, ref } from "vue";

  const input = ref();
  const output = ref<string>("");

  var websocket: WebSocket | undefined = undefined;

  function onMessage(ev: MessageEvent) {
    const data = JSON.parse(ev.data);

    output.value += data.output;
  }

  // function onSocketDisconnect() {}

  // function onSocketOpen(e) {}

  function execute() {
    if (websocket) {
      websocket.send(JSON.stringify({ input: input.value }));
    }
  }
  onMounted(() => {
    const ws = new WebSocket(adminSocketURL + "?admin_key=" + getAdminCookie());
    websocket = ws;
    websocket.onmessage = onMessage;
    // websocket.onclose = onSocketDisconnect
    // websocket.onopen = onSocketOpen
  });
</script>

<template>
  <div class="h-1/2 p-1 gap-x-2 lg:flex relative">
    <textarea
      v-model="input"
      spellcheck="false"
      placeholder="Type commands to excute"
      aria-expanded="false"
      class="tarea placeholder:opacity-20 font-semibold"
      id=""
      cols="30"
      rows="10"
    ></textarea>

    <button
      @click="execute"
      class="absolute btn btn-sm bottom-5 right-5 btn-primary"
    >
      RUN
    </button>

    <textarea
      id="console-output"
      v-model="output"
      aria-expanded="false"
      class="tarea"
      cols="30"
      rows="10"
    ></textarea>
  </div>
</template>

<style>
  .tarea {
    @apply w-full p-1 h-full resize-none ring-2 focus:ring-secondary bg-base-100 focus:outline-none rounded-md;
  }
</style>
