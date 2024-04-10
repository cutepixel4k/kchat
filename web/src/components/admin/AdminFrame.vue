<script setup lang="ts">
  import SettingsPannel from "./SettingsPannel.vue";
  import { ref } from "vue";
  import RoomSettings from "./room/RoomSettings.vue";

  const menu = ["App", "Rooms"];
  const current = ref(menu[0]);

  function changeTab(item: any) {
    current.value = item;
  }
</script>

<template>
  <div class="h-full w-full flex flex-col lg:flex-row">
    <!-- SettingsMenu -->
    <div class="lg:h-full lg:w-1/4 bg-base-300 lg:block">
      <div class="w-full overflow-y-auto tabs tabs-boxed">
        <div
          v-for="item in menu"
          :class="item === current ? ' tab-active' : ''"
          role="tablist"
          class="hover:cursor-pointer hover:bg-base-100 tab font-semibold"
          @click="changeTab(item)"
        >
          {{ item }}
        </div>
      </div>
    </div>
    <!-- SettingsPannel -->
    <div class="flex-1 bg-base-100">
      <SettingsPannel v-show="current === 'App'" />
      <RoomSettings v-show="current === 'Rooms'" />
    </div>
  </div>
</template>
