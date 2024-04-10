<script setup lang="ts">
  import { onMounted, ref } from "vue";
  import axios from "axios";
  import { onBeforeMount } from "vue";
  import { useRoute } from "vue-router";
  import { backendURL } from "@/api/socket";
  import type { JoinUserInterface, createUserInterface } from "@/api/ktypes";

  const action = ref();
  const roomDetails = ref<{
    roomID: string;
    roomName: string;
    roomUsername: string;
    hasPassword: boolean;
  }>();

  const roomName = ref("");

  const username = ref("");
  const password = ref(undefined);
  const isPublic = ref(false);

  const route = useRoute();

  const props = defineProps(["joinUser", "createUser", "error"]);
  const error = ref(props.error);

  function inputChecks(tp: "create" | "join") {
    const usplit = username.value.trim().split(" ");
    // ----------------------
    if (usplit[0].length < 4 || usplit[0].length > 12) {
      error.value = "username must be 4 - 8 characters 😑";
      return false;
    } else if (usplit.length > 1) {
      error.value = "username must not contain spaces 😫";
      return false;
    }
    if (tp === "create") {
      // --------------------- creation checks
      if (roomName.value.length < 3 || roomName.value.length > 20) {
        error.value = "Room name must be 3 - 20 characters 😑";
        return false;
      }
    }
    return true;
  }

  function createRoom() {
    if (inputChecks("create")) {
      const user: createUserInterface = {
        username: username.value,
        roomName: roomName.value,
        password: password.value,
        isPublic: isPublic.value,
      };
      props.createUser(user);
    }
  }
  // on user request to Join
  function joinRoom() {
    if (roomDetails.value?.roomID) {
      if (inputChecks("join")) {
        const user: JoinUserInterface = {
          username: username.value,
          password: password.value,
          roomID: roomDetails.value?.roomID,
        };
        props.joinUser(user);
      }
    }
  }

  function connectRoom() {
    if (action.value === "create") {
      // ------------------------
      createRoom();
    } else if (action.value == "join") {
      // -------------------------
      joinRoom();
    }
  }

  // exit if route error
  onBeforeMount(() => {
    action.value = route.params.action;

    if (action.value === "join") {
      axios
        .get(backendURL + "/api/room/details", {
          params: { room_id: route.query.roomID },
        })
        .then((res) => {
          roomDetails.value = res.data.details;
        });
    }
  });
</script>

<template>
  <!-- popup -->
  <div class="h-full w-full flex justify-center md:items-center p-4">
    <!-- join user -->
    <div class="card w-full md:w-1/2 flex flex-col gap-2">
      <!-- room details -->
      <div
        class="border-x-2 border-t-2 shadow-2xl rounded-lg p-1 flex flex-col gap-2 skeleton bg-base-300"
        v-if="action === 'join'"
      >
        <h1 class="text-center rounded-md font-bold">
          {{ roomDetails?.roomName }}
        </h1>
        <hr class="border-base-content" />
        <div class="text-end px-2 font-semibold flex justify-between">
          <h1 class="text-secondary">
            Password : {{ roomDetails?.hasPassword ? "Yes" : "No" }}
          </h1>
          <h1 class="text-primary">
            Created By {{ roomDetails?.roomUsername }}
          </h1>
        </div>
      </div>

      <div
        v-else
        class="p-2 ring-2 bg-base-300 text-context-content font-semibold text-center rounded-lg skeleton"
      >
        CREATE ROOM
      </div>

      <h1 class="text-error animate-bounce break-words">{{ error }}</h1>
      <!-- <a href="/" class="link link-success">Return HOME</a> -->

      <!-- username -->
      <input
        v-model="username"
        autofocus="true"
        class="input input-primary h-10 mb-1"
        type="search"
        placeholder="Username"
      />
      <!-- create room -->

      <div class="w-full">
        <!-- create user render -->
        <div v-if="action === 'create'" class="w-full">
          <div class="w-full flex gap-2">
            <input
              v-model="roomName"
              class="input input-primary w-full h-10"
              type="text"
              placeholder="Room Name"
            />
            <input
              v-model="password"
              class="input input-primary w-full h-10"
              type="text"
              placeholder="Password (optional)"
            />
          </div>

          <div class="w-full flex justify-end p-2 gap-3">
            <h1 class="font-semibold">PUBLIC</h1>

            <input
              v-model="isPublic"
              class="checkbox checkbox-primary bg-base border-info"
              type="checkbox"
            />
          </div>
        </div>

        <input
          v-if="roomDetails?.hasPassword"
          v-model="password"
          class="input input-primary"
          type="text"
          placeholder="Enter Password"
        />

        <button
          @click="connectRoom"
          class="btn btn-outline w-full btn-info h-10"
        >
          {{ action === "create" ? "CREATE" : "JOIN" }}
        </button>
        <a href="/" class="btn btn-link h-10">GO BACK</a>
      </div>
    </div>
    <!-- create user -->
  </div>
</template>
