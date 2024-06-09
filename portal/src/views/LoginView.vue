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

  const check_password = ref(true)
  function showPassword(){
    var password = document.getElementById("password");
    if (password.type === "password") {
      password.type = "text";
      check_password.value = false;
    } else {
      password.type = "password";
      check_password.value = true;
    }
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
          <div class="relative mb-7">
              <input
                id="password"
                type="password"
                v-model="data.password"
                placeholder="Ingrese su contraseña"
                required
                class="block w-full transition duration-300 px-5 py-4 text-sm font-medium outline-none rounded-2xl shadow-md shadow-indigo-50 bg-indigo-50 hover:bg-indigo-100 focus:bg-indigo-200 text-gray-900 placeholder:text-gray-700"
              />
              <div class="absolute inset-y-0 end-0 flex items-center pe-3 cursor-pointer">
                <svg @click="showPassword" v-if="check_password" class="w-5 h-5 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 18">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1.933 10.909A4.357 4.357 0 0 1 1 9c0-1 4-6 9-6m7.6 3.8A5.068 5.068 0 0 1 19 9c0 1-3 6-9 6-.314 0-.62-.014-.918-.04M2 17 18 1m-5 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
                </svg>
                <svg @click="showPassword" v-else class="w-5 h-5 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 14">
                  <g stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                    <path d="M10 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>
                    <path d="M10 13c4.97 0 9-2.686 9-6s-4.03-6-9-6-9 2.686-9 6 4.03 6 9 6Z"/>
                  </g>
                </svg>
              </div>
          </div>
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
          <a href="http://localhost:5000/login" target="_blank">
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