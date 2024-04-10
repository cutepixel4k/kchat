import { onMounted, ref } from "vue";
import { defineStore } from "pinia";

export const useAdminStore = defineStore("admin", () => {
  const loggedIn = ref(false);
  const adminDetails = ref<{
    key: string;
    name: string;
  }>();

  return { adminDetails, loggedIn };
});
