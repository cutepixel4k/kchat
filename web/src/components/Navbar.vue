<script setup lang="ts">
  import { onBeforeMount, onMounted, ref } from "vue";
  // import Sidebar from "@/components/sub/Sidebar.vue";
  import { useAdminStore } from "@/stores/admin";
  import { getCookie, setCookie } from "@/api/admin";

  const props = defineProps(["title"]);

  const theme = ref("dracula");
  const adminStore = useAdminStore();

  const themes = [
    "light",
    "dark",
    "cupcake",
    "bumblebee",
    "emerald",
    "corporate",
    "synthwave",
    "retro",
    "cyberpunk",
    "valentine",
    "halloween",
    "garden",
    "forest",
    "aqua",
    "lofi",
    "pastel",
    "fantasy",
    "wireframe",
    "black",
    "luxury",
    "dracula",
    "cmyk",
    "autumn",
    "business",
    "acid",
    "lemonade",
    "night",
    "coffee",
    "winter",
    "dim",
    "nord",
    "sunset",
  ];

  function selectTheme(name: string) {
    theme.value = name;
    document.body.setAttribute("data-theme", name);
    setCookie("theme", name, 1);
  }

  onMounted(() => {
    const dTheme = getCookie("theme");
    if (dTheme) {
      theme.value = dTheme;
    }
  });
</script>

<template>
  <div
    class="shadow-lg bg-gradient-to-br from-secondary to-info flex justify-between p-3 items-center"
  >
    <!-- title -->
    <a href="/" class="flex items-center gap-1 text-secondary-content">
      <img src="/icon.png" alt="icon" class="w-10 h-10" />
      <h1 class="font-bold">{{ props.title }}</h1>
      <h1 class="font-bold" v-if="adminStore.loggedIn">
        | ADMIN ><span class="">
          {{ adminStore.adminDetails?.name }}
        </span>
      </h1>
    </a>

    <div class="flex items-center gap-2 text-info-content">
      <!-- Themes -->
      <div class="dropdown dropdown-end items-center top-1 z-50">
        <button tabindex="0" class="">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="25"
            height="25"
            fill="currentColor"
            class="bi bi-palette"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3m4 3a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3M5.5 7a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m.5 6a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"
            />
            <path
              d="M16 8c0 3.15-1.866 2.585-3.567 2.07C11.42 9.763 10.465 9.473 10 10c-.603.683-.475 1.819-.351 2.92C9.826 14.495 9.996 16 8 16a8 8 0 1 1 8-8m-8 7c.611 0 .654-.171.655-.176.078-.146.124-.464.07-1.119-.014-.168-.037-.37-.061-.591-.052-.464-.112-1.005-.118-1.462-.01-.707.083-1.61.704-2.314.369-.417.845-.578 1.272-.618.404-.038.812.026 1.16.104.343.077.702.186 1.025.284l.028.008c.346.105.658.199.953.266.653.148.904.083.991.024C14.717 9.38 15 9.161 15 8a7 7 0 1 0-7 7"
            />
          </svg>
        </button>
        <!-- <div tabindex="0" role="button" class="btn">Click</div> -->
        <ul
          tabindex="0"
          class="dropdown-content right-0 p-4 shadow max-h-52 overflow-y-auto bg-base-100 text-base-content rounded-box w-40 space-y-2"
        >
          <li
            @click="selectTheme(t)"
            v-for="t in themes"
            class="uppercase hover:cursor-pointer hover:text-secondary"
            :class="theme === t ? 'text-primary' : ''"
          >
            <a>{{ t }}</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
