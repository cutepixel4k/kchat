<script setup lang="ts">
  import axios from "axios";
  import { onBeforeMount, onUpdated, ref } from "vue";
  import { backendURL } from "@/api/socket";
  import { getAdminCookie } from "@/api/admin";

  const props = defineProps(["roomID", "isAdmin", "myname"]);

  const members = ref([]);
  const open = ref(false);

  function getRoomUsers() {
    axios
      .get(backendURL + "/api/room/members", {
        params: { room_id: props.roomID },
      })
      .then((res) => {
        members.value = res.data.members;
      });
  }

  function toogleOpen() {
    // if not open then fetch
    if (!open.value) {
      getRoomUsers();
    }

    open.value = !open.value;
  }
  function kickMember(member: string) {
    axios
      .get(backendURL + "/api/admin/room/remove", {
        params: {
          key: getAdminCookie(),
          room_id: props.roomID,
          username: member,
        },
      })
      .then((res) => {
        getRoomUsers();
      });
  }
</script>

<template>
  <div class="w-full">
    <!-- header -->
    <div
      @click="toogleOpen"
      class="header p-2 flex items-center justify-between px-3 hover:cursor-pointer"
    >
      <!-- left buttons -->
      <div class="flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          class="bi bi-people-fill"
          viewBox="0 0 16 16"
        >
          <path
            d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5.784 6A2.24 2.24 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.3 6.3 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"
          />
        </svg>
        <h1>MEMBERS</h1>
      </div>
      <!-- right arrow -->
      <div>
        <svg
          v-if="open"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="currentColor"
          class="bi bi-caret-down"
          viewBox="0 0 16 16"
        >
          <path
            d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"
          />
        </svg>
        <!-- arrow right -->
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="currentColor"
          class="bi bi-caret-right"
          viewBox="0 0 16 16"
        >
          <path
            d="M6 12.796V3.204L11.481 8zm.659.753 5.48-4.796a1 1 0 0 0 0-1.506L6.66 2.451C6.011 1.885 5 2.345 5 3.204v9.592a1 1 0 0 0 1.659.753"
          />
        </svg>
      </div>
    </div>

    <!-- admin -->

    <!-- content -->
    <div v-if="open" class="h-52 w-full overflow-y-auto p-1">
      <!-- all users -->
      <div v-for="member in members" class="flex justify-between px-2">
        <h1>{{ member }}</h1>
        <button
          v-if="props.isAdmin && props.myname !== member"
          @click="kickMember(member)"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
            class="bi bi-x-lg"
            viewBox="0 0 16 16"
          >
            <path
              d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .header {
    background-color: rgba(50, 0, 50, 0.3);
  }
</style>
