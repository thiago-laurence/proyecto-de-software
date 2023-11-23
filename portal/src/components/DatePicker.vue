<template>
    <flat-pickr
        class=" col-span-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Seleccione una fecha"
        name="date"
        v-model="selectedDate"  
        >
        <div class="relative">
            <input
            :config="config"
            />
        </div>
    </flat-pickr>
</template>

<script setup>
    import flatPickr from 'vue-flatpickr-component';
    import 'flatpickr/dist/flatpickr.css';
    import { ref } from 'vue';

    const selectedDate = ref(null); // Define la variable reactiva para el v-model

    const expose = { selectedDate };
</script>