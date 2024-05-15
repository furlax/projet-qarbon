import { createRouter, createWebHashHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import { LOCALSTORAGE_TOKEN_KEY } from "../services/authService"

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView
  },
  {
    path: "/my-events",
    name: "my-events",
    component: () => import("../views/MyEventsView.vue")

  },
  {
    path: "/myinbox",
    name: "myinbox",
    component: () => import("../views/MyInboxView.vue")
  },
  // {
  //   path: "/messages",
  //   name: "messages",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ "../views/MessagesView.vue")
  // },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue")
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/RegisterView.vue")
  },
  {
    path: "/create-place",
    name: "create-place",
    component: () => import("../views/CreatePlaceView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/event-create",
    name: "event-create",
    component: () => import("../views/EventCreateView.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/event-list",
    name: "event-list",
    component: () => import("../views/EventsView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: "/place-list",
    name: "place-list",
    component: () => import("../views/PlaceView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: "/place-detail/:id",
    name: "place-detail",
    component: () => import("../views/PlaceDetailView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: "/event-detail/:id",
    name: "event-detail",
    component: () => import("../views/EventDetailView.vue"),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const isAuthenticated = localStorage.getItem(LOCALSTORAGE_TOKEN_KEY)
  console.log(isAuthenticated)

  if (requiresAuth && !isAuthenticated) {
    next("/login") // or wherever you want to redirect unauthenticated users
  } else {
    next()
  }
})

export default router
