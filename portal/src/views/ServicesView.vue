<template>
    <!-- Buscador -->
    <div class="services-search p-4 m-5">
        <h1 class="flex items-center text-5xl font-extrabold">Services<span class="bg-blue-100 text-blue-800 text-2xl font-semibold mr-2 px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ml-2">Search</span></h1>
        <br>
        <form @submit.prevent="searchServices" action>
            <div class="flex">
                <label for="search-dropdown" class="mb-2 text-sm font-medium text-gray-900 sr-only"></label>
                <select id="dropdown-button" class=" py-2.5 px-4 text-sm font-medium text-gray-900 bg-gray-100 border border-gray-300 rounded-l-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600" >
                    <option value="" disabled selected>Tipo</option>
                    <option value="">All</option>
                    <option v-for="type in services_types" :key="type.id" :value="type.id">
                        {{ type.name }}
                    </option>
                </select>
                <div class="relative w-full">
                    <input type="search" id="search-dropdown" class="block p-2.5 w-full z-20 text-sm text-gray-900 bg-gray-50 rounded-r-lg border-l-gray-50 border-l-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-l-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500" placeholder="Revestimiento, pintura ...">
                    <button type="submit" class="absolute top-0 right-0 p-2.5 text-sm font-medium h-full text-white bg-blue-700 rounded-r-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                        </svg>
                        <span class="sr-only">Search</span>
                    </button>
                </div>
            </div>
        </form>
        <br>
        <!-- Services list -->
        <p id="aviso" style="display: none" class="text-center text-gray-500 dark:text-white">No se encontraron servicios</p>
        <div>
            <Service  v-for="service in servicios" :key="service.id" :service="service">
                <template #name> {{ service.name }} </template>
                <template #description> {{ service.info }} </template>
                <template #route>
                    <RouterLink :to="'/service/' + service.id">Ver servicio</RouterLink>
                </template>     
            </Service>
        </div>
        <!-- Pagination -->
        <div v-if="servicios" class="flex items-center justify-center">
            <button @click="anteriorPag" class="flex items-center justify-center px-3 h-8 mr-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                <svg class="w-3.5 h-3.5 mr-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5H1m0 0 4 4M1 5l4-4"/>
                </svg>
                Anterior
            </button>
            <span class="mr-3 text-sm font-medium text-gray-500 dark:text-white">{{ currentPage }}</span>
            <button @click=" siguientePag" class="flex items-center justify-center px-3 h-8 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                Siguiente
                <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                </svg>
            </button>
        </div>
    </div>

</template>

<script setup>
    import { ref,onMounted } from 'vue';
    import { API } from '@/api'
    import Service from './../components/Service.vue';

    let servicios = ref(null);
    let currentPage = ref(1);
    let perPage = ref(10);
    let services_types = ref(null);
    
    //obtiene tipos de servicio y su id de la api
    onMounted(async () => {
        try {
            const response = await API.get('services/services-types');
            services_types.value = response.data;
        } catch (error) {
            console.error('Error al obtener tipos de servicios:', error);
            throw error; // Propagar el error para manejarlo en el componente
        }
        try {
            const response2 = await API.get('services/search?q=');
            servicios.value = response2.data.data;
        } catch (error) {
            console.error('Error al obtener servicios:', error);
            throw error; // Propagar el error para manejarlo en el componente
        }
    });

    function checkParams(type, query){
        if(type == null || type == ''){
            type = '';
        }
        else{
            if(type != ''){
                let tipo = services_types.value.find(obj => obj.id == type);
                if(tipo == null){
                    type = '';
                }
            }
        }
        if(query == null || query == ''){
            query = '';
        }
        return [type, query];
    }

    //busca servicios por tipo y una query pegandole a la api
    function searchServices(page){
        let type = document.getElementById('dropdown-button').value;
        let query = document.getElementById('search-dropdown').value;
        [type, query] = checkParams(type, query);
        
        let url = '/services/search?q='+query+'&type='+type+'&page='+page+'&per_page='+perPage.value;

        API.get(url)
        .then(response => {
            if(response.data.error){
                currentPage.value--;
            }
            else{
                if(response.data.data){
                    document.getElementById('aviso').style.display = 'none';
                    servicios.value = response.data.data;
                }
                else{
                    document.getElementById('aviso').style.display = 'block';
                    servicios.value = null;
                }
            }
        })
        .catch(error => {
            console.log(error)
        })
    }

    function siguientePag(){
        currentPage.value++;
        searchServices(currentPage.value);
    }
    function anteriorPag(){
        if(currentPage.value > 1){
            currentPage.value--;
        }
        searchServices(currentPage.value);
    }

</script>
