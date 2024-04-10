<script setup lang="ts">
  import { backendURL } from "@/api/socket";
  import anime from "animejs";
  import axios from "axios";
  import { onBeforeMount, onBeforeUpdate, onMounted, ref } from "vue";

  var members: string[] = [];

  const found = ref<string[]>([]);
  const props = defineProps(["roomID", "onUserSelect", "username"]);

  const loading = ref(true);

  function change(v: string) {
    if (v.trimEnd() !== v) {
      console.log("space press");
    }

    found.value = [];
    if (v.trim().length === 0) {
      found.value = members;
      return;
    }
    members.forEach((e) => {
      if (e.startsWith(v.trim())) {
        // -----
        found.value.push(e);
      }
    });
  }

  onMounted(() => {
    anime({
      targets: document.getElementById("mention-bar"),
      translateY: [100, 0],
    });
    // ------------------------
    axios
      .get(backendURL + "/api/room/members", {
        params: { room_id: props.roomID },
      })
      .then((r) => {
        const values = r.data;
        members = values.members;
        found.value = members;

        loading.value = false;
      });
  });

  onBeforeUpdate(() => {});

  defineExpose({ change });
</script>

<template>
  <div
    id="mention-bar"
    class="w-full h-28 -z-50 rounded-t-lg border-2 border-b-0 border-secondary flex flex-col overflow-y-auto relative"
  >
    <div v-if="loading" class="w-full h-full flex items-center justify-center">
      <!-- loading data -->
      <span class="loading loading-ring loading-lg"></span>
    </div>
    <!-- all members -->

    <div v-else v-for="m in found" class="px-4 hover:cursor-pointer">
      <!-- name -->
      <div class="flex justify-between p-1">
        <h1 class="truncate font-smibold">{{ m }}</h1>
        <div class="flex gap-2" v-if="props.username !== m">
          <!-- broadcast -->
          <button
            @click="props.onUserSelect(m, 0)"
            class="bg-primary px-2 rounded-lg p-1 text-primary-content"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              fill="currentColor"
              class="bi bi-megaphone-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M13 2.5a1.5 1.5 0 0 1 3 0v11a1.5 1.5 0 0 1-3 0zm-1 .724c-2.067.95-4.539 1.481-7 1.656v6.237a25 25 0 0 1 1.088.085c2.053.204 4.038.668 5.912 1.56zm-8 7.841V4.934c-.68.027-1.399.043-2.008.053A2.02 2.02 0 0 0 0 7v2c0 1.106.896 1.996 1.994 2.009l.496.008a64 64 0 0 1 1.51.048m1.39 1.081q.428.032.85.078l.253 1.69a1 1 0 0 1-.983 1.187h-.548a1 1 0 0 1-.916-.599l-1.314-2.48a66 66 0 0 1 1.692.064q.491.026.966.06"
              />
            </svg>
          </button>
          <!-- secret -->
          <button
            @click="props.onUserSelect(m, 1)"
            class="bg-secondary px-2 rounded-lg p-1 text-secondary-content"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              fill="currentColor"
              class="bi bi-chat-heart-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6-.097 1.016-.417 2.13-.771 2.966-.079.186.074.394.273.362 2.256-.37 3.597-.938 4.18-1.234A9 9 0 0 0 8 15m0-9.007c1.664-1.711 5.825 1.283 0 5.132-5.825-3.85-1.664-6.843 0-5.132"
              />
            </svg>
          </button>
        </div>
        <!-- actions -->
      </div>
    </div>
    <!-- Explaining user -->
  </div>
</template>
