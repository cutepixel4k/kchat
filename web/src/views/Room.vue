<script setup lang="ts">
  import type { createUserInterface, JoinUserInterface } from "@/api/ktypes";
  import Chat from "@/components/chat/Chat.vue";
  import JoinChat from "@/components/chat/JoinChat.vue";
  import Navbar from "@/components/Navbar.vue";
  import { ref } from "vue";

  const showLogin = ref(true);
  const error = ref();

  const createUserData = ref<createUserInterface>();
  const joinUserData = ref<JoinUserInterface>();

  // called by chat component after user succesfully connected
  function onSuccess() {
    // loading.value = false;
  }

  function onClose(r: string) {
    // ------------------- if closed
    error.value = r;
    showLogin.value = true;
  }

  function create(user: createUserInterface) {
    createUserData.value = user;
    showLogin.value = false;
  }
  function join(user: JoinUserInterface) {
    joinUserData.value = user;
    showLogin.value = false;
  }
</script>
<template>
  <main class="h-screen flex flex-col overflow-hidden">
    <!-- navbar -->
    <Navbar title="KCHAT" />
    <JoinChat v-if="showLogin" :joinUser="join" :createUser="create" :error />
    <!-- chat -->
    <Chat
      v-else
      :create="createUserData"
      :join="joinUserData"
      :onSuccess
      :onClose
    />
  </main>
</template>
