<script setup>
  import { ref } from 'vue'
  import { useUserStore } from '@/stores/user'
  import { googleSdkLoaded } from "vue3-google-login"
  
  const user = useUserStore()
  const data = {
    email: '',
    password: '',
  }
  const error = ref(false)
  const msg = ref('')

  async function login() {
    await user.login(data.email, data.password)
      .then(response => {
        data.password = ''
        data.email = ''
        error.value = false
        window.location.href = '/'

        return response
      })
      .catch(response => {
        if (!response.ok){
          error.value = true
          msg.value = 'El usuario o contraseña son incorrectos'
        }
      });
  }

  async function check_login(response){
    await user.login_google(response)
      .then(response => {
        msg.value = ''
        error.value = false
        window.location.href = '/'

        return response
      })
      .catch(response => {
        if (!response.ok){
          error.value = true
          msg.value = response.response.data.error
        }
      });
  }

  const auth_google = () => {
    googleSdkLoaded((google) => {
      google.accounts.oauth2.initTokenClient({
      client_id: '835796648231-pbl9o1302ab9t1doeo1cqmu2ptdm47b3.apps.googleusercontent.com',
      scope: 'email profile openid',
      callback: (response) => {
        check_login(response)
      }
      }).requestAccessToken()
    })
  }



</script>

<template>  
  <div class="bg-indigo-100 md:px-20 md:py-10 py-2" v-if="!user.isLoggedIn">
    <div class="bg-white rounded-md shadow-xl text-center p-10 flex items-center justify-center">
      <div class="xl:px-40 xl:w-2/3 w-full md:px-20">
        <h1 class="lg:text-5xl text-3xl text-gray-900 font-extrabold">Iniciar sesión</h1>
        <p class="mt-4 text-gray-700">Ingrese su usuario y contraseña</p>
        <form @submit.prevent="login" class="flex flex-col w-full h-full pt-6 text-center">
          <button type="button" @click="auth_google" class="flex items-center justify-center py-3 mb-6 text-base font-medium transition duration-300 rounded-2xl shadow-lg border shadow-indigo-100 text-gray-900 bg-white hover:bg-indigo-50 focus:ring-1 focus:ring-indigo-300">
            <img class="h-6 mr-2" src="@/assets/img/logo-google.png" alt="logo-google" />
            Iniciar sesión con Google
          </button>
          
          <div class="flex items-center mb-3">
            <hr class="h-0 border-b border-solid border-gray-400 grow" />
            <p class="mx-4 text-gray-500">or</p>
            <hr class="h-0 border-b border-solid border-gray-400 grow" />
          </div>
          <label for="#user.email" class="mb-2 text-base text-start text-gray-900"> Usuario </label>
          <input
            id="email"
            type="email"
            v-model="data.email"
            placeholder="email@example.com"
            required
            class="flex items-center transition duration-300 px-5 py-4 mr-2 mb-7 text-sm font-medium outline-none rounded-2xl shadow-md shadow-indigo-50 bg-indigo-50 hover:bg-indigo-100 focus:bg-indigo-200 text-gray-900 placeholder:text-gray-700"
          />
          <label for="#user.password" class="mb-2 text-base text-start text-gray-900"> Contraseña </label>
          <input
            id="password"
            type="password"
            v-model="data.password"
            placeholder="Ingrese su contraseña"
            required
            class="flex items-center transition duration-300 px-5 py-4 mr-2 mb-7 text-sm font-medium outline-none rounded-2xl shadow-md shadow-indigo-50 bg-indigo-50 hover:bg-indigo-100 focus:bg-indigo-200 text-gray-900 placeholder:text-gray-700"
          />
          <div v-if="error" class="text-red-500 mb-4 text-base font-medium bg-red-50 rounded-full">
            <p>{{ msg }}</p>
          </div>
          <div class="flex flex-row justify-between mb-8">
            <label class="relative inline-flex items-center mr-3 cursor-pointer select-none">
              <input
                type="checkbox"
                class="w-5 h-5 bg-white border-2 rounded-sm border-gray-500"
                value=""
              />
              <span class="ml-3 text-sm font-normal text-gray-900">Recuerdame</span>
            </label>
            <a
              href="javascript:void(0)"
              class="mr-4 text-sm font-medium text-indigo-500 transition duration-300 hover:underline p-1 rounded-xl"
              >¿Olvidaste tu contraseña?</a
            >
          </div>
          <button
            type="submit"
            class="w-full py-4 mb-6 text-base font-bold leading-none text-white transition duration-300 rounded-2xl hover:bg-indigo-600 focus:ring-4 focus:ring-indigo-200 bg-indigo-500"
          >
            Iniciar sesión
          </button>
          <p class="text-sm leading-relaxed text-gray-900">
            <RouterLink to="sign-up">
              ¿Aún no estas registrado?
              <a
                class="font-bold text-gray-700 ml-2 rounded-lg transition duration-300 hover:bg-indigo-50 focus:bg-indigo-100 p-2"
              >
                Crear cuenta
              </a>
            </RouterLink>
          </p>
          <div class="flex items-center my-5">
            <hr class="h-0 border-b border-solid border-gray-400 grow" />
          </div>
          <a href="https://admin-grupo10.proyecto2023.linti.unlp.edu.ar/login" target="_blank">
            <button
              type="button"
              class="w-3/4 py-2 mb-3 text-sm font-bold leading-none text-white transition duration-300 rounded-2xl hover:bg-violet-600 focus:ring-4 focus:ring-violet-200 bg-violet-500"
            >
              Administración
            </button>
          </a>
        </form>
      </div>
    </div>
  </div>
</template>