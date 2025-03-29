<template>
    <div class="w-full">
      <label :for="id" class="block text-sm font-medium text-gray-700 mb-1">{{ label }}</label>
      <input 
        :id="id"
        :type="type"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="w-full px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-300"
        :class="{'border-red-500': error}"
      />
      <!-- Display error message if any -->
      <p v-if="error" class="text-sm text-red-500 mt-1">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
    defineProps({
      id: String,
      label: String,
      type: { type: String, default: "text" },
      placeholder: String,
      modelValue: String,
      error: String,
    });
    
    defineEmits(["update:modelValue"]);
  </script>
  