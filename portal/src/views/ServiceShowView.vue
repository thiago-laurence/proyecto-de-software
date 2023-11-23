<script>
import { API } from '@/api';
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user'
import L from 'leaflet';

const user = useUserStore()

let service = ref(null);

export default {
    setup() {
        const user = useUserStore();

        return {
            user
        };
    },
    data() {
        return {
            service: null
        };
    },
    async mounted() {
        const id = this.$route.params.id; // Accede al parámetro id de la URL actual
        await API.get('/services/' + id)
            .then(response => {
                this.service = response.data;
            })
            .catch(error => {
                console.error('Error al cargar el servicio:', error);
            });
        //comienza muestreo de mapa
        const coordenadas = this.service.institution.localization.split(',');
        let c;
        if (coordenadas.length == 2) { //si la institucion tiene coordenadas "validas" las pongo, sino uso unas por defecto
            c = [coordenadas[0], coordenadas[1]];
        }
        else {
            c = [-34.933333, -57.95];
        }
        var map = L.map('map').setView(c, 13);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        L.marker(c).addTo(map)
            .bindPopup('Nos podes encontrar acá.<br> Te esperamos!')
            .openPopup();
    }
};
</script>

<template>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    </head>
    <div v-if="service" class="box-content mx-auto mt-40">
        <div v-if="service" class="bg-white border m-6 rounded-lg shadow-2xl shadow-black">
            <div class="flex flex-col w-full flex-wrap">

                <div class="flex flex-col  lg:flex-row w-full md:px-10 items-center justify-between mt-10">
                    <div class="flex flex-col w-9/10">
                        <h3 class="text-xl lg:text-5xl font-extrabold dark:text-white">Servicio {{ service.name }}</h3>
                    </div>

                    <div class="flex flex-col w-1/10  m-5">
                        <button
                            class=" text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
                            type="button">
                            <RouterLink :to="/create-order/ + service.id" v-if="user.isLoggedIn">Solicitar</RouterLink>
                            <RouterLink to="/login" v-if="!user.isLoggedIn">Solicitar</RouterLink>
                            <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 14 10">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M1 5h12m0 0L9 1m4 4L9 9" />
                            </svg>
                        </button>
                    </div>
                </div>


                <br>
                <div class="h-1 w-full bg-indigo-500 rounded"></div>
                 <div class="flex w-full justify-between px-5 flex-col lg:flex-row mt-10 py-5">
                    <div class="flex flex-col mx-4">
                        <div class="w-full">
                            <dt class="text-2xl mb-2 font-semibold leading-none text-gray-900 dark:text-white lg:text-start text-center">
                                Detalles del servicio: </dt>
                            <dd class="text-xl mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400 lg:text-start text-center">{{
                                service.info }}</dd>
                            <dt class="text-2xl mb-2 font-semibold leading-none text-gray-900 dark:text-white lg:text-start text-center">
                                Institucion: </dt>
                            <dd class="text-xl mb-4 font-light text-gray-500 sm:mb-5 dark:text-gray-400 lg:text-start text-center">{{
                                service.institution.name }}</dd>
                        </div>
                    </div>

                    <div class="flex flex-col max-lg:w-full lg:w-2/3 justify-center">
                        <p class="text-2xl text-gray-500 dark:text-white text-center">¿Cómo llegar?</p>
                        <br>
                        <div class="w-full h-96">
                            <div id="map" style="height: 100%; width: 100%;"></div>
                        </div>
                    </div>
                </div>
               
            </div>


    </div>
</div></template>

