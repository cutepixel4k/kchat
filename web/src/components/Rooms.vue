<script setup lang="ts">
  import { backendURL } from "@/api/socket";
  import axios from "axios";
  import { onMounted, ref } from "vue";
  import { useRouter } from "vue-router";

  const router = useRouter();

  interface RoomData {
    roomID: string;
    roomName: string;
    roomUsername: string;
    hasPassword: boolean;

    roomLimit: string;
  }

  const rooms = ref<RoomData[]>([]);
  const vipRooms = ref<RoomData[]>([]);
  const search = ref("");
  const showSearch = ref(false);

  const searching = ref(false);

  function roomJoin(roomID: string | undefined) {
    // check errors future
    router.push({ path: "room/join", query: { roomID } });
  }

  function createRoom() {
    router.push({ path: "room/create" });
  }

  function searchRoom() {
    if (search.value === undefined || searching.value) {
      return;
    }
    // ----------------------
    searching.value = true;
    axios
      .get(backendURL + "/api/rooms/search", {
        params: {
          room_name: search.value,
        },
      })
      .then((res) => {
        vipRooms.value = res.data.vip_rooms;
        rooms.value = res.data.rooms;
        searching.value = false;
      });
  }

  onMounted(() => {
    searchRoom();
  });
</script>

<template>
  <div class="h-screen flex flex-col p-2 overflow-y-auto">
    <div class="w-full flex gap-2 items-center p-2 justify-between">
      <h1>VIP ROOMS</h1>
      <!-- line will be replaced -->
      <div class="border-t-2 flex-1 border-info"></div>
      <button
        @click="showSearch = !showSearch"
        class="btn btn-primary btn-sm text-primary-content"
      >
        SEARCH ROOM
      </button>
    </div>
    <!-- search -->
    <div
      v-if="showSearch"
      class="flex justify-between mb-2 w-full px-1 gap-4 relative items-center"
    >
      <input
        v-model="search"
        type="text"
        class="flex-1 focus:outline-none rounded-lg p-1 ring-2 bg-base-100 px-3"
        placeholder="Type room name here"
      />
      <!-- search icon -->

      <button
        @click="searchRoom"
        class="p-2 absolute right-2 flex items-center"
      >
        <div v-if="searching" class="loading loading-spinner"></div>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          class="bi bi-search-heart"
          viewBox="0 0 16 16"
        >
          <path
            d="M6.5 4.482c1.664-1.673 5.825 1.254 0 5.018-5.825-3.764-1.664-6.69 0-5.018"
          />
          <path
            d="M13 6.5a6.47 6.47 0 0 1-1.258 3.844q.06.044.115.098l3.85 3.85a1 1 0 0 1-1.414 1.415l-3.85-3.85a1 1 0 0 1-.1-.115h.002A6.5 6.5 0 1 1 13 6.5M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11"
          />
        </svg>
      </button>
    </div>
    <!-- main room -->
    <h1
      v-if="vipRooms?.length === 0"
      class="flex-1 flex items-center justify-center w-full"
    >
      No rooms available
    </h1>
    <!-- courcel -->
    <div v-else class="w-full carousel carousel-end rounded-box gap-2">
      <div
        v-for="room in vipRooms"
        class="carousel-item w-full text-secondary-content flex bg-gradient-to-b from-accent/80 to-purple-500 bg-primary relative"
        :class="vipRooms.length === 1 ? 'w-full' : 'md:w-1/2'"
      >
        <div class="card-body glass backdrop-blur-sm">
          <div class="card-title justify-center">{{ room.roomName }}</div>
          <hr class="border-accent-content" />
          <p class="font-semibold">Created by | {{ room?.roomUsername }}</p>
          <p>ACTIVE [ {{ room.roomLimit }} ]</p>
          <div class="card-actions justify-end">
            <button @click="roomJoin(room?.roomID)" class="btn btn-sm">
              JOIN
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- public rooms -->
    <div class="w-full flex gap-2 items-center p-2">
      <h1>PUBLIC ROOMS</h1>
      <div class="border-t-2 flex-1 border-info"></div>
      <button @click="createRoom" class="btn btn-info btn-sm text-info-content">
        CREATE ROOM
      </button>
    </div>
    <!-- public rooms -->
    <h1
      v-if="rooms.length === 0"
      class="flex-1 flex items-center justify-center"
    >
      No rooms available
    </h1>
    <!-- show this -->
    <div v-else class="flex-1 flex flex-wrap overflow-y-auto">
      <!-- rooms -->
      <div class="card p-1 w-1/2 md:w-1/4" v-for="(room, i) in rooms">
        <div
          @click="roomJoin(room.roomID)"
          :class="i % 2 === 0 ? 'bg-secondary/40' : 'bg-primary/40'"
          class="card-body shadow-lg rounded-lg border-2 hover:border-base-content hover:cursor-pointer border-primary-content"
        >
          <div class="card-title">{{ room.roomName }}</div>
          <p>{{ room.roomUsername }}</p>
          <p>{{ room.roomLimit }}</p>
          <p>Password : {{ room.hasPassword ? "Yes" : "No" }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .c-skeleton {
    animation: skeleton 1.8s ease-in-out infinite;

    background-size: 200% auto;
    background-repeat: no-repeat;
    background-position-x: -20%;
  }
</style>
