import { api, socketapi } from "./config";
// remove
// var socket: WebSocket | undefined = undefined;

// -------------------------------------------------------- self hosting
// const host = document.location.host;
// const protocol = document.location.protocol;

// const ws = protocol === "https:" ? "wss" : "ws";

// const backendURL = `${protocol}//${host}`;
// const socketURL = `${ws}://${document.location.host}/ws/room`;
// const adminSocketURL = `${ws}://${document.location.host}/ws/admin`;
// ----------------------------------------------------------------- different host
const backendURL = api;
const socketURL = `${socketapi}/ws/room`;
const adminSocketURL = `${socketapi}/ws/admin`;

function createConnection(
  username: string,
  roomName: string,
  password: string | undefined = undefined,
  isPublic: boolean
) {
  var newURL = `${socketURL}/create/${username}?room_name=${roomName}`;
  if (password !== undefined) {
    newURL += "&password=" + password;
  }
  if (isPublic) {
    newURL += "&private=no";
  }

  return newURL;
}
function joinConnection(
  username: string,
  roomID: string,
  password: string | undefined = undefined
) {
  var newURL = `${socketURL}/join/${username}?room_id=${roomID}`;
  if (password !== undefined) {
    newURL += "&password=" + password;
  }

  return newURL;
}

export { backendURL, createConnection, joinConnection, adminSocketURL };
