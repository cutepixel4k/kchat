interface Message {
  notify: boolean; // if its a notify message
  username: string; // username of sender socket
  self: boolean; // if the message for self
  message: any; // message object dynamic
  msgid: string; // message id generated from server
}

interface Setting {
  label: string;
  key: string;
  value: any;

  desc: string;
  hint: string;
  tp: string;
}

interface createUserInterface {
  username: string;
  roomName: string;
  password: undefined | string;
  isPublic: boolean;
}
interface JoinUserInterface {
  username: string;
  roomID: string;
  password: undefined | string;
}

export type { Message, Setting, createUserInterface, JoinUserInterface };
