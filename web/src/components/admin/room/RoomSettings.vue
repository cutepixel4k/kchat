<script setup lang="ts">
  import { ref } from "vue";
  import RoomDetails from "./RoomDetails.vue";
  import RoomLiveLogs from "./RoomLiveLogs.vue";
  import RoomSearch from "./RoomSearch.vue";

  const roomDetails = ref();

  function getDetails(roomID: string) {
    roomDetails.value.fetchRoomDetails(roomID);
  }
</script>

<template>
  <div class="w-full h-full flex flex-col">
    <!-- label -->
    <RoomSearch :getDetails />
    <div class="flex-1 overflow-y-auto lg:overflow-hidden">
      <RoomDetails ref="roomDetails" />
      <RoomLiveLogs />
    </div>
  </div>
</template>
