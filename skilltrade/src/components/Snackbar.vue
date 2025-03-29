<template>
  <transition name="fade">
    <div 
      v-if="show" 
      :class="snackbarClass"
      class="fixed bottom-5 right-5 px-4 py-2 rounded-lg shadow-lg text-white"
    >
      {{ message }}
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from "vue";

const show = ref(false);
const message = ref("");
const type = ref("success"); 

const snackbarClass = computed(() => ({
  "bg-green-500": type.value === "success",
  "bg-red-500": type.value === "error",
}));

const showSnackbar = (msg, msgType = "success", duration = 3000) => {
  message.value = msg;
  type.value = msgType;
  show.value = true;
  setTimeout(() => {
    show.value = false;
  }, duration);
};

defineExpose({ showSnackbar });
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
