<template>
    <Notifications
        v-for="notification in notifications"
        :type="notification.type"
        :message="notification.message"
    />
    <!-- Modal content -->
    <div class="relative p-4 bg-white dark:bg-gray-800 sm:p-5 mx-auto my-auto max-w-7xl">
        <!-- Modal header -->
        <div class="flex justify-between items-center pb-4 mb-4 rounded-t border-b sm:mb-5 dark:border-gray-600">
            <h3 class="text-3xl font-semibold text-gray-900 dark:text-white">
                Solicitar servicio
            </h3>
        </div>
        <!-- Modal body -->
        <form @submit.prevent="create_order">
            <div class="gap-4 mb-4">
                <div>
                    <label for="#order.title" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Título</label>
                    <input type="text" name="title" id="title" v-model="data.title" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Título de la solicitud" required>
                </div>

                <br>
                <div date-rangepicker class="items-center">
                    <div class="relative">
                        <label for="#order.creation_date">Fecha desde</label>
                        <DatePicker v-model="data.creation_date"/>
                    </div>
                    <br>
                    <div class="relative">
                        <label for="#order.close_date">Fecha hasta</label>
                        <DatePicker v-model="data.close_date"/>
                    </div>
                </div>
                <br>
                <div class="sm:col-span-2">
                    <label for="#order.description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Descripción de la solicitud</label>
                    <textarea id="description" name="description" v-model="data.description" rows="4" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Escriba la descripción aquí" required></textarea>                    
                </div>
            </div>
            <br>
            <button type="submit" class="text-white inline-flex items-center bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                <svg class="mr-1 -ml-1 w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path></svg>
                Solicitar servicio
            </button>
        </form>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import { API } from '@/api'
    import { useRoute } from 'vue-router';
    import { useUserStore } from '@/stores/user';
    import flatPickr from 'vue-flatpickr-component';
    import 'flatpickr/dist/flatpickr.css';
    import Notifications from '../components/Notifications.vue';
    import DatePicker from '../components/DatePicker.vue'

    let notifications = ref([]);

    let data = ref({
        title: '',
        description: '',
        creation_date: '',
        close_date: '',
        service_id: '',
    })
    let user = useUserStore();  

    const route = useRoute();
    data.value.service_id = route.params.id;

    function parseFecha(fecha) {
      const partes = fecha.split('-');
      if (partes.length === 3) {
        const anio = parseInt(partes[0], 10);
        const mes = parseInt(partes[1], 10) - 1; // Resta 1 al mes ya que en JavaScript los meses van de 0 a 11
        const dia = parseInt(partes[2], 10);

        const fecha = new Date(anio, mes, dia);

        return fecha;
      }
      else {
        return null;
      }
    }

    function checkParams(){
        data.value.creation_date = parseFecha(data.value.creation_date);
        data.value.close_date = parseFecha(data.value.close_date);

        if(data.value.title === '' || data.value.description === '' || data.value.creation_date === '' || data.value.close_date === '' || data.value.service_id === ''){
            notifications.value.push({
                type: 'error',
                message: 'Debe completar todos los campos',
            });
            return false;
        }
        else{
            if(data.value.creation_date === null || data.value.close_date === null) {
                notifications.value.push({
                    type: 'error',
                    message: 'Formato de fecha incorrecto',
                });
                return false;
            }
            else{
                if(data.value.creation_date > data.value.close_date) {
                    notifications.value.push({
                        type: 'info',
                        message: 'La fecha de cierre debe ser mayor a la de inicio',
                    });
                    return false;
                }
            }
        }
        return true;
    }
    
    async function create_order() {

        if(checkParams() === false){
            return;
        }
        else{

            await API.post('/me/requests', data.value)
            .then(response => {
                if(response.status === 201){
                    notifications.value.push({
                        type: 'success',
                        message: 'Orden creada correctamente',
                    });
                    data.value.title = '';
                    data.value.description = '';
                    data.value.creation_date = '';
                    data.value.close_date = '';
                    data.value.service_id = '';

                    window.location.href = '/service-orders';
                }
                else{
                    notifications.value.push({
                        type: 'danger',
                        message: 'Problema al crear la orden: '+response.data.msg,
                    });
                }
            })
            .catch(error => {   
                if(error.response.data.msg === "Token has expired"){
                    user.logout();
                    window.location.href = '/login';
                }
                else{
                    notifications.value.push({
                        type: 'error',
                        message: 'Error al crear la orden: '+error.response.data.msg
                    });
                }
            });
        }
    } 
</script>