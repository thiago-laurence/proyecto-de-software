<script setup>
import TextImg from '../components/TextImg.vue';
import InfoIcon from '../components/InfoIcon.vue'
import { ref, onMounted } from 'vue';
import { API } from '@/api'

const text_information = 'Somos una institución que se dedica a la obtención de nuevos desarrollos tecnológicos relativos a pinturas y recubrimientos protectores, en aspectos de interés nacional y provincial.';
const text_services = 'Contamos con muchos centros en los cuáles se ofrecen distintos servicios que podrían interesarte. En el apartado de servicios podras realizar búsquedas para encontrar lo que necesites.';
const text_institutions = "Visualiza fácilmente que ofrece cada centro de investigación."
const text_search = 'Inicia solicitudes de servicios rápidamente y desde la comodidad de tu casa.'

var contact = ref();

onMounted(async () => {
  try {
    const response = await API.get('contact/');
    let data = response.data
    contact.value = data.split(';')
  } catch (error) {
    console.error('Error al obtener informacion de contacto:', error);
  }
});

</script>

<template>
  <main class="w-full principal py-10">
    <div class="flex flex-col flex-wrap items-center  justify-center">
      <div class="flex xl:flex-row flex-col">
        <div class="flex flex-col lg:h-screen w-full  justify-center items-center">
          <div class="flex flex-row h-2/5 max-xl:mb-2 ">
            <h1 class="title font-light  text-white text-center mb-10 mx-6 drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
              CENTRO DE INVESTIGACIÓN Y DESARROLLO EN TECNOLOGÍA DE PINTURAS Y RECUBRIMIENTOS
            </h1>
          </div>

          <div
            class="flex flex-row flex-wrap justify-center items-center bg-gradient-to-r from-gray-900 to-violet-600 p-2 rounded-lg mx-10">

            <div class="flex flex-col">
              <h3 class="font-light text-gray-100 text-center text-3xl drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
                Bienvenido al portal web de CIDEPINT, conocé más sobre nosotros y en que podemos ayudarte
              </h3>
            </div>


          </div>

          <div class="flex flex-row mt-3 justify-center items-center">
            <div class="flex flex-col">
              <span class="material-symbols-outlined text-gray-100 text-5xl">
                keyboard_arrow_down
              </span>
            </div>
            <div class="flex flex-col">
              <span class="material-symbols-outlined text-gray-100 text-5xl">
                keyboard_arrow_down
              </span>
            </div>
            <div class="flex flex-col">
              <span class="material-symbols-outlined text-gray-100 text-5xl">
                keyboard_arrow_down
              </span>
            </div>
          </div>
        </div>
        <div class="flex flex-wrap lg:flex-col w-3/4 pt-16 ml-16 max-xl:hidden">
            <div>
              <img src="../assets/img/fondo6-removebg.png">
            </div>
        </div>
      </div>

    <div class="flex flex-row bg-indigo-100 w-4/5 h-1 mx rounded-lg"></div>
    <div class="flex flex-row mt-10 mx-10 justify-center text-gray-100 items-center">
      <TextImg direction="flex-row" :text="text_information" icon="info"></TextImg>
    </div>
    <div class="flex flex-row mt-10 justify-center mx-10 text-gray-100 items-center">
      <TextImg direction="flex-row-reverse" :text="text_services" icon="travel_explore"></TextImg>
    </div>


    <div class="flex flex-row mt-10 justify-center mx-10 text-gray-100 items-center">
      <div class="flex flex-col mr-5">
        <TextImg direction="flex-row" :text="text_institutions" icon="visibility"></TextImg>
      </div>
        <div class="flex flex-col ml-5">
          <TextImg direction="flex-row" :text="text_search" icon="bolt"></TextImg>
        </div>
      </div>
      <div class="flex flex-row my-10 bg-indigo-100 w-4/5 h-1 mx rounded-lg"></div>
      <div class="flex flex-row mt-1">
        <h2 class="title font-light text-gray-100 text-center mb-10 drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
          CONTACTO
        </h2>
      </div>
      <!-- <div class="flex flex-row justify-center text-gray-100 items-center">
            <InfoIcon icon="location_on" text="Av. 52 s/n entre 121 y 122 B1900AYP La Plata, Buenos Aires"></InfoIcon>
        </div>
        <div class="flex flex-row mt-6 justify-center mx-10 text-gray-100 items-center">
            <InfoIcon icon="mail" text="Dirección: direccion@cidepint.ing.unlp.edu.ar"></InfoIcon>
        </div>
        <div class="flex flex-row mt-6 justify-center mx-10 text-gray-100 items-center">
            <InfoIcon icon="mail" text="Servicios a terceros: servicios@cidepint.ing.unlp.edu.ar"></InfoIcon>
        </div>
        <div class="flex flex-row mt-6 justify-center mx-10 text-gray-100 items-center">
            <InfoIcon icon="phone" text="+54 0221 421-2433"></InfoIcon>
        </div>
        <div class="flex flex-row mt-6 justify-center mx-10 text-gray-100 items-center">
            <InfoIcon icon="phone" text="WhatsApp (solo mensajes): : +54 0221 357-1205"></InfoIcon>
        </div> -->
      <div v-for="(item, index) in contact"
        class="flex flex-row text-center justify-center mt-1 text-gray-100 items-center">
        {{ item }}

      </div>
    </div>
  </main>
</template>

<style scoped>
.principal {
  background-image: url('../assets/img/fondo2.jpg');
  background-repeat: repeat;
}

.title {
  font-size: 5ch;
}
</style>
