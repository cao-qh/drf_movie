import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MovieDetail from "../views/MovieDetail.vue";
import Register from "../views/Register.vue";
import Login from "../views/Login.vue";
import Personal from "../views/Personal.vue";
import ResetPassword from "@/views/ResetPassword.vue";
import PasswordReset from "@/views/PasswordReset.vue";
import ChangePassword from "../views/ChangePassword.vue";
import store from "../store";
import ActivateEmail from "../views/ActivateEmail.vue";
import MemberCard from "../views/MemberCard.vue";
import Collect from "../views/Collect.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/movie/:id",
    name: "MovieDetail",
    component: MovieDetail,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },

  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/reset_password",
    name: "ResetPassword",
    component: ResetPassword,
  },
  {
    path: "/password_reset/:uid/:token",
    name: "PasswordReset",
    component: PasswordReset,
  },
  {
    path: "/activate/:uid/:token",
    name: "ActivateEmail",
    component: ActivateEmail,
  },

  {
    path: "/personal",
    name: "Personal",
    component: Personal,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/change_password",
    name: "ChangePassword",
    component: ChangePassword,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/collect",
    name: "Collect",
    component: Collect,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/member_card",
    name: "MemberCard",
    component: MemberCard,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

const token = localStorage.getItem("token");
if (token) {
  store.commit("setLoginStatus", true);
}

router.beforeEach((to, from, next) => {
  if (store.state.isLogin && (to.name === "Login" || to.name === "Register")) {
    next({ name: "home" });
  } else if (
    to.matched.some((record) => record.meta.requireLogin) &&
    !store.state.isLogin
  ) {
    next({ name: "Login", query: { jump: to.path } });
  } else {
    next();
  }
});

export default router;
