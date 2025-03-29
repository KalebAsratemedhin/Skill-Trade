<template>
    <button 
      class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition"
      :disabled="disabled"
    >
      <slot></slot>
    </button>
</template>
  
<script setup>
  defineProps({
    disabled: Boolean,
  });
</script>
  