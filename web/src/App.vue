<script setup lang="ts">
  import { onBeforeMount, onMounted } from "vue";
  import { RouterView } from "vue-router";
  import { useAdminStore } from "./stores/admin";
  import {
    getAdminCookie,
    setAdminCookie,
    deteAdminCookie,
    getCookie,
  } from "./api/admin";
  import axios from "axios";
  import { backendURL } from "./api/socket";

  const adminStore = useAdminStore();

  function verifyAdmin(key: string) {
    // check admin in start of app
    axios
      .get(backendURL + "/api/admin/check_key", { params: { key } })
      .then((res) => {
        if (res.data.res === "ok") {
          // all good store admin key in store
          adminStore.adminDetails = { key, name: res.data.name };
          adminStore.loggedIn = true;
          setAdminCookie(key);
        } else {
          adminStore.loggedIn = false;
        }
      })
      .catch(() => {
        deteAdminCookie();
      });
  }

  onMounted(() => {
    const key = getAdminCookie();
    if (key) {
      verifyAdmin(key);
    }
  });

  onBeforeMount(() => {
    const theme = getCookie("theme");
    if (theme) {
      document.body.setAttribute("data-theme", theme);
    }
  });
</script>

<template>
  <RouterView />
</template>
