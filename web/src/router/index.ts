import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import Room from "../views/Room.vue";
import Random from "@/views/Random.vue";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/room/:action",
      name: "room",
      component: Room,
    },
    {
      path: "/random",
      name: "random",
      component: Random,
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("../views/Admin.vue"),
    },
    {
      path: "/error",
      name: "error",
      component: () => import("../views/Error.vue"),
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
  ],
});

export default router;
