import { createRouter, createWebHistory } from "vue-router";
import SignUp from "@/pages/SignUp.vue";
import SignIn from "@/pages/SignIn.vue";
import Dashboard from "@/pages/Dashboard.vue";
import { useAuthStore } from "../store/auth";


const routes = [
  { 
    path: "/signup", 
    name: "signup",
    component: SignUp 
},
  { 
    path: "/signin",
    name: "signin",
    component: SignIn 
},
{ 
  path: "/dashboard",
  name: "dashboard",
  component: Dashboard,
  meta: { requiresAuth: true } 
},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  console.log("is authenticatedd", authStore.isAuthenticated)
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      next("/signin"); // Redirect to SignIn if not authenticated
  } else {
      next(); // Proceed to route
  }
});

export default router;
