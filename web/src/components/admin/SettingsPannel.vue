<script setup lang="ts">
  import { onMounted, ref } from "vue";
  import InputBox from "./InputBox.vue";
  import type { Setting } from "@/api/ktypes";
  import axios from "axios";
  import { getAdminCookie } from "@/api/admin";
  import { backendURL } from "@/api/socket";

  const settings = ref<Setting[]>([]);
  const res = ref<{ code: number; reason: string }>();

  const URL = `${backendURL}/api/admin/settings`;
  const postURL = `${URL}?admin_key=${getAdminCookie()}`;

  function submit() {
    const form = document.forms[0];

    // Convert form data to key-value object
    const formData = new FormData(form);
    const dataObject: { [key: string]: string } = {};

    formData.forEach((value, key) => {
      dataObject[key] = value.toString();
    });
    axios
      .post(postURL, {
        body: dataObject,
      })
      .then((r) => {
        res.value = {
          code: r.status,
          reason: r.statusText,
        };
      })
      .catch((r) => {
        res.value = {
          code: r.status,
          reason: r.statusText,
        };
      });
  }

  onMounted(() => {
    axios
      .get(URL, {
        params: { admin_key: getAdminCookie() },
      })
      .then((res) => {
        settings.value = res.data.settings;
      })
      .catch((res) => {
        console.log("error ", res);
      });
  });
</script>

<template>
  <div class="w-full h-full flex flex-col relative">
    <div
      v-if="res"
      class="relative glass rounded-md animate-pulse"
      :class="
        res.code === 200
          ? 'bg-success/80 text-success-content'
          : 'bg-error/80 text-error-content'
      "
    >
      <div class="p-1 text-center font-semibold flex-1">
        {{ res.reason }}
        <button class="absolute right-2 top-2" @click="res = undefined">
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
    <!-- dynamic buttons -->

    <form
      class="flex-1 p-2 overflow-y-auto flex flex-col"
      :action="postURL"
      method="post"
    >
      <InputBox v-for="setting in settings" :setting />
    </form>

    <div
      class="w-full flex fixed bottom-0 lg:static z-50 justify-end px-4 py-2 gap-2 text-primary-content"
    >
      <button
        @click="submit"
        class="btn btn-primary btn-sm w-16 text-accent-content shadow-xl"
      >
        Save
      </button>
    </div>
  </div>
</template>
