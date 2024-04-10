<script setup lang="ts">
  import { backendURL } from "@/api/socket";
  import Navbar from "@/components/Navbar.vue";
  import AdminFrame from "@/components/admin/AdminFrame.vue";
  import AdminLogin from "@/components/admin/AdminLogin.vue";
  import axios from "axios";

  import { setAdminCookie } from "@/api/admin";

  import { useAdminStore } from "@/stores/admin";

  const adminStore = useAdminStore();

  function verifyAdmin(key: string) {
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
      });
  }

  function onLogin(key: string) {
    verifyAdmin(key);
  }
</script>

<template>
  <div class="h-screen flex flex-col overflow-hidden">
    <Navbar />
    <div class="flex-1 overflow-hidden">
      <AdminLogin v-if="!adminStore.loggedIn" :login="onLogin" />
      <AdminFrame v-else />
    </div>
  </div>
</template>
