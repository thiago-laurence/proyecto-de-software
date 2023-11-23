<template>
    <br>
    <div class=" m-5">
        <form @submit.prevent="searchOrders">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div>
                    <label for="#data.creation_date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Rango de fechas:</label>
                    <div class="grid grid-cols-11">
                        <DatePicker v-model="data.creation_date" />
                        <span class="col-span-1 text-center mt-4">to</span>
                        <DatePicker v-model="data.close_date" />
                    </div>
                </div>
                <div>
                    <label for="#data.status" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Estado:</label>
                    <select v-model="data.status" id="status" name="status" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                        <option value="" disabled selected>Estado</option>
                        <option value="">All</option>
                        <option  v-for="state in orders_states" :key="state.id" :value="state.id">
                            {{ state.name }}
                        </option>
                    </select>
                </div>
                <div>
                    <label for="#data.order" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Orden de búsqueda:</label>
                    <select v-model="data.order" id="order" name="order" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required>
                        <option value="" disabled selected>Orden</option>
                        <option value="asc">Ascendente</option>
                        <option value="desc">Descendente</option>
                    </select>
                </div>
                <div >
                    <label for="#data.sort" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Criterio de búsqueda:</label>
                    <select v-model="data.sort" id="sort" name="sort" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required>
                        <option value="" disabled selected>Filtrar por...</option>
                        <option value="creation_date">Fecha de comienzo</option>
                        <option value="close_date">Fecha de fin</option>
                    </select>
                    <br> 
                    <button type="submit" class="text-white absolute right-4 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-normal rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        Buscar
                    </button>
                </div>    
            </div>
        </form>
        <br>
        <br>
        <Notifications
            v-for="notification in notifications"
            :type="notification.type"
            :message="notification.message"
        />
        <!-- Pagination -->
        <div v-if="orders" class="flex items-center justify-center">
            <button @click="anteriorPag" class="flex items-center justify-center px-3 h-8 mr-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                <svg class="w-3.5 h-3.5 mr-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5H1m0 0 4 4M1 5l4-4"/>
                </svg>
                Anterior
            </button>
            <span class="mr-3 text-sm font-medium text-gray-500 dark:text-white">{{ data.page }}</span>
            <button @click=" siguientePag" class="flex items-center justify-center px-3 h-8 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                Siguiente
                <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                </svg>
            </button>
        </div>
        <br>
        <p id="aviso" style="display: none" class="text-center text-gray-500 dark:text-white">No se encontraron solicitudes de servicio</p>
        <div v-if="orders" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 ">
            <ServiceOrder v-for="order in orders.data" :key="order.id">
                <template #status>
                    {{order.status_changes[0].service_order_status.name}}
                </template>
                <template #title>
                    {{ order.title }}
                </template>
                <template #creation_date>
                    {{ order.creation_date.split('T')[0] }}
                </template>
                <template #close_date>
                    {{ order.close_date.split('T')[0] }}
                </template>
                <template #description>
                    {{ order.description }}
                </template>
                <template #route>
                    <RouterLink :to="'/service-order/' + order.id">Notas</RouterLink>
                </template>
            </ServiceOrder>
        </div>
    </div>
    
</template>

<script setup>
    import { ref,onMounted } from 'vue';
    import { API } from '@/api';
    import flatPickr from 'vue-flatpickr-component';
    import 'flatpickr/dist/flatpickr.css';
    import ServiceOrder from './../components/ServiceOrder.vue';
    import Notifications from '../components/Notifications.vue';
    import DatePicker from '../components/DatePicker.vue';
    import { useUserStore } from '@/stores/user';

    let orders_states = ref(null);
    let orders = ref(null);
    let notifications = ref([]);
    //let currentPage = ref(1);
    let user = useUserStore();  

    let data = ref({
        sort: "",
        order: "",
        status: "",
        creation_date: "",
        close_date: "",
        page:1,
        per_page:10
    });
    
    //obtiene los estados de las ordenes de servicio junto con sus ids
    onMounted(async () => {
        try {
            const response = await API.get('services/orders-state');
            orders_states.value = response.data;
        } catch (error) {
            console.error('Error al obtener estados de ordenes:', error);
            throw error; // Propagar el error para manejarlo en el componente
        }
        try {
            const resp2 = await API.get('me/requests');
            orders.value = resp2.data[0];
        } catch (error) {
            notifications.value.push({
                type: 'info',
                message: 'Debe iniciar sesión para ver sus solicitudes de servicio',
            });
        }
    });
    function checkParams(){
        if(data.value.sort == "" || data.value.order == ""){
            notifications.value.push({
                type: 'error',
                message: 'Debe completar los campos de criterio y orden de busqueda',
            });
            return false;
        }
        return true;
    }

    async function searchOrders(){
        if(!checkParams()){
            return;
        }
        let url = '/me/requests?sort='+data.value.sort+'&order='+data.value.order+'&status='+data.value.status+'&creation_date='+data.value.creation_date+'&close_date='+data.value.close_date+'&page='+data.value.page+'&per_page='+data.value.per_page;

        await API.get(url)
        .then(response => {

            if(response.data){
                if(response.data[0].data.length > 0){
                    document.getElementById("aviso").style.display = "none";
                    orders.value = response.data[0];
                }
                else{
                    document.getElementById("aviso").style.display = "block";
                    orders.value = null;
                }
            }
            
        })
        .catch(error => {
            if(error.response.data.error == "No hay elementos en esa pagina"){
                data.value.page--;
            }
            else{
                if(error.response.data.msg == "Token has expired"){
                    user.logout();
                    window.location.href = '/login';
                }
            }
        });
    }

    //paginacion
    function siguientePag(){
        //currentPage.value++;
        data.value.page++;
        searchOrders();
        
    }
    function anteriorPag(){
        if(data.value.page > 1){
            //currentPage.value--;
            data.value.page--;
        }
        searchOrders();
    }


</script>