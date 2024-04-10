<script setup lang="ts">
  import { backendURL } from "@/api/socket";
  import axios from "axios";
  import { onMounted, ref } from "vue";

  const props = defineProps(["roomID"]);

  const membersList = ref([]);
  const details = ref({});

  function fetchRoomDetails(roomID: string) {
    axios
      .get(backendURL + "/api/room/members", {
        params: { room_id: roomID },
      })
      .then((res) => {
        membersList.value = res.data.members;
      });

    axios
      .get(backendURL + "/api/admin/room/details", {
        params: { room_id: roomID },
      })
      .then((res) => {
        details.value = res.data.details;
      });
  }

  function removeMember(name: string) {
    // -----------------------------
  }

  defineExpose({ fetchRoomDetails });
</script>

<template>
  <!-- room deatils -->
  <div
    class="w-full h-full lg:h-1/2 flex flex-wrap lg:flex-nowrap gap-2 py-2 px-1"
  >
    <!-- details -->
    <div
      class="overflow-x-auto h-1/2 w-full lg:h-full lg:w-1/2 ring-2 rounded-lg"
    >
      <table class="table">
        <!-- head -->
        <thead>
          <tr>
            <th>Name</th>
            <th>Detail</th>
          </tr>
        </thead>
        <tbody>
          <!-- row 1 -->
          <tr v-for="(k, v) in details">
            <td>{{ v }}</td>
            <td>{{ k }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- members -->
    <div
      class="overflow-x-auto h-1/2 w-full lg:h-full lg:w-1/2 ring-2 rounded-lg"
    >
      <table class="table">
        <!-- head -->
        <thead>
          <tr>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          <!-- row 1 -->
          <tr v-for="member in membersList">
            <td class="w-full flex justify-between">
              <!-- button -->
              {{ member }}
              <button @click="removeMember(member)">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  fill="currentColor"
                  class="bi bi-person-x"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4m.256 7a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z"
                  />
                  <path
                    d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m-.646-4.854.646.647.646-.647a.5.5 0 0 1 .708.708l-.647.646.647.646a.5.5 0 0 1-.708.708l-.646-.647-.646.647a.5.5 0 0 1-.708-.708l.647-.646-.647-.646a.5.5 0 0 1 .708-.708"
                  />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
