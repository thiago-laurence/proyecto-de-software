<script setup>
import PieChart from '@/components/PieChart.vue'
import BarChart from '@/components/BarChart.vue'
import BubbleChart from '@/components/BubbleChart.vue'
</script>

<template>
    <div class="p-8 bg-indigo-50">
        <div class="flex felx-col items-center justify-center">
            <span class="rounded-full bg-indigo-500 px-4 py-1 text-white font-bold uppercase text-sm">
                Estadísticas
            </span>
        </div>
        <h1 class="font-extrabold text-gray-700 text-center mt-6 sm:text-xl md:text-2xl lg:text-5xl">
            Análisis de datos de CIDEPINT
        </h1>
        <p class="text-center mt-6 text-lg font-light text-gray-500">
            Información pública sobre el uso de la plataforma para fines cientificos y estadisticos
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3">
        <div class="p-8">
            <div class="bg-indigo-100 rounded-full w-16 h-16 flex justify-center items-center text-indigo-500 shadow-2xl">
                <svg class="w-8 h-8" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                    viewBox="0 0 22 21">
                    <path
                        d="M16.975 11H10V4.025a1 1 0 0 0-1.066-.998 8.5 8.5 0 1 0 9.039 9.039.999.999 0 0 0-1-1.066h.002Z" />
                    <path
                        d="M12.5 0c-.157 0-.311.01-.565.027A1 1 0 0 0 11 1.02V10h8.975a1 1 0 0 0 1-.935c.013-.188.028-.374.028-.565A8.51 8.51 0 0 0 12.5 0Z" />
                </svg>
            </div>
            <h2 class="uppercase mt-6 text-indigo-500 font-medium mb-3">
                Cantidad de solicitudes
            </h2>
            <p class="font-light text-base text-gray-500 mb-3">
                Clasificación de servicios por tipo y su cantidad de solicitudes procesadas.
            </p>
        </div>

        <div class="p-8">
            <div class="bg-green-100 rounded-full w-16 h-16 flex justify-center items-center text-green-500 shadow-2xl">
                <svg class="w-8 h-8" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 16">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M1 1v14h16M4 10l3-4 4 4 5-5m0 0h-3.207M16 5v3.207" />
                </svg>
            </div>
            <h2 class="uppercase mt-6 text-green-500 font-medium mb-3">
                Servicios más solicitados
            </h2>
            <p class="font-light text-base text-gray-500 mb-3">
                Recopilación de los cinco servicios más solicitados por los usuarios de la plataforma.
            </p>
        </div>
        <div class="p-8">
            <div class="bg-red-100 rounded-full w-16 h-16 flex justify-center items-center text-red-500 shadow-2xl">
                <svg class="h-8 w-8" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linejoin="round" stroke-width="2"
                        d="M10 6v4l3.276 3.276M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
            </div>
            <h2 class="uppercase mt-6 text-red-500 font-medium mb-3">
                Instituciones con mejor tiempo de resolución
            </h2>
            <p class="font-light text-base text-gray-500">
                Recopilación de las diez instituciones cientificas con mejores tiempos de resolución de solicitudes
                recibidas por parte de los usuarios.
            </p>
        </div>
    </div>

    <div class="grid grid-cols-1  lg:grid-cols-3 content-start items-strech my-4">
        <div class="bg-indigo-50 rounded-xl p-2 m-4 shadow-lg shadow-indigo-300">
            <div class="flex flex-col">
                <div class="flex flex-row justify-center h-2/3 items-center">
                    <div class="flex justify-center w-full lg:h-80">
                        <PieChart />
                    </div>
                </div>
                <div class="flex flex-row justify-center h-1/3 items-center">
                    <p class="text-base font-normal text-gray-600 mt-8 p-4 h-full bg-gray-200 rounded-xl">
                        "Análisis", "Consultoria", "Desarrollo" corresponden a los tipos de solicitudes registradas, junto a
                        la cantidad de
                        solicitudes procesadas para cada uno.
                    </p>
                </div>
            </div>

        </div>
        
        <div class="bg-green-50 rounded-xl p-2 m-4 shadow-lg shadow-green-300">
            <div class="flex flex-col">
                <div class="flex flex-row justify-center h-2/3 items-center">
                    <div class="flex justify-center w-full lg:h-80">
                        <BarChart />
                    </div>
                </div>
                <div class="flex flex-row justify-center h-1/3 items-center">
                    <p class="text-base font-normal text-gray-600 mt-8 p-4 bg-gray-200 rounded-xl">
                        Servicio solicitado e institución que lo brinda, junto a la cantidad de solicitudes procesadas para el mismo.
                    </p>
                </div>
            </div>
        </div>
        <div class="bg-red-50 rounded-xl p-2 m-4 shadow-lg shadow-red-300">
            <div class="flex flex-col">
                <div class="flex flex-row justify-center h-2/3 items-center">
                    <div class="flex justify-center w-full lg:h-80">
                        <BubbleChart />
                    </div>
                </div>
                <div class="flex flex-row justify-center h-1/3 items-center">
                    <p class="text-base font-normal text-gray-600 mt-8 p-4 bg-gray-200 rounded-xl">
                        Tiempo de resolución: Tiempo promedio que tarda una institución en responder una solicitud. <br>
                        Los tiempos son aproximados en cantidad de dias (eje X) y horas (eje Y) (dd:hh).
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
