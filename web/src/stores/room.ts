import { ref } from "vue";
import { defineStore } from "pinia";
import type { Message } from "@/api/ktypes";

export const useRoomStore = defineStore("room", () => {
  const roomID = ref(); // Joined room id
  const inRoom = ref(false); // User in room ?
  const username = ref(); // current username
  // const clearTimer = ref(0);

  // replyMessage for mentioning TODO optimize
  const replyMessage = ref<Message>();

  return { roomID, inRoom, replyMessage, username };
});
