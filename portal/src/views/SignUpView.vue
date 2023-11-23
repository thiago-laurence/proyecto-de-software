<script setup>
  import { ref } from 'vue'
  import { useUserStore } from '@/stores/user'
  import { googleSdkLoaded } from "vue3-google-login"

  const user = useUserStore()
  const data = {
    email: '',
    name: '',
    lastname: ''
  }
  const error = ref(false)
  const success = ref(false)
  const msg = ref('')

  async function sign_up() {
    await user.sign_up(data.email, data.name, data.lastname)
      .then(response => {
        data.email = ''
        data.name = ''
        data.lastname = ''
        error.value = false
        success.value = true
        msg.value = response.data.success

        return response
      })
      .catch(response => {
        if (!response.ok){
          error.value = true
          success.value = false
          msg.value = response.response.data.error
        }
      });
  }

  async function check_login(response){
    await user.login_google(response)
      .then(response => {
        msg.value = ''
        data.email = ''
        data.name = ''
        data.lastname = ''
        error.value = false
        success.value = false
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
        <h1 class="lg:text-5xl text-3xl text-gray-900 font-extrabold">Crear una cuenta</h1>
        <p class="mt-4 text-gray-700">Complete el formulario</p>
        <form action @submit.prevent="sign_up" method="POST" class="flex flex-col w-full h-full pt-6 text-center">
          <button type="button" @click="auth_google" class="flex items-center justify-center py-3 mb-6 text-base font-medium transition duration-300 rounded-2xl shadow-lg border shadow-indigo-100 text-gray-900 bg-white hover:bg-indigo-50 focus:ring-1 focus:ring-indigo-300">
              <img class="h-6 mr-2" src="@/assets/img/logo-google.png" alt="logo-google" />
              Registrarse con Google
          </button>
          <div class="flex items-center mb-3">
            <hr class="h-0 border-b border-solid border-gray-400 grow" />
            <p class="mx-4 text-gray-500">or</p>
            <hr class="h-0 border-b border-solid border-gray-400 grow" />
          </div>
          <label for="email" class="mb-2 text-base text-start text-gray-900"> Email </label>
          <input
            id="email"
            type="email"
            placeholder="email@example.com"
            v-model="data.email"
            required
            maxlength="50"
            class="flex items-center transition duration-300 px-5 py-4 mr-2 mb-7 text-sm font-medium outline-none rounded-2xl shadow-md shadow-indigo-50 bg-indigo-50 hover:bg-indigo-100 focus:bg-indigo-200 text-gray-900 placeholder:text-gray-700"
          />
          <label for="email" class="mb-2 text-base text-start text-gray-900"> Nombre </label>
          <input
            id="name"
            type="text"
            placeholder="John"
            v-model="data.name"
            required
            maxlength="50"
            class="flex items-center transition duration-300 px-5 py-4 mr-2 mb-7 text-sm font-medium outline-none rounded-2xl shadow-md shadow-indigo-50 bg-indigo-50 hover:bg-indigo-100 focus:bg-indigo-200 text-gray-900 placeholder:text-gray-700"
          />
          <label for="lastname" class="mb-2 text-base text-start text-gray-900"> Apellido </label>
          <input
            id="lastname"
            type="text"
            placeholder="Doe"
            v-model="data.lastname"
            required
            maxlength="50"
            class="flex items-center transition duration-300 px-5 py-4 mr-2 mb-7 text-sm font-medium outline-none rounded-2xl shadow-md shadow-indigo-50 bg-indigo-50 hover:bg-indigo-100 focus:bg-indigo-200 text-gray-900 placeholder:text-gray-700"
          />
          <div v-if="error" class="text-red-500 mb-4 text-base font-medium bg-red-50 rounded-full">
            <p>{{ msg }}</p>
          </div>
          <div v-if="success" class="text-emerald-500 mb-4 text-base font-medium bg-red-50 rounded-full">
            <p>{{ msg }}</p>
          </div>
          <button
            type="submit"
            class="w-full py-4 mb-6 text-base font-bold leading-none text-white transition duration-300 rounded-2xl hover:bg-indigo-600 focus:ring-4 focus:ring-indigo-200 bg-indigo-500"
          >
            Registrarse
          </button>
          <p class="text-sm leading-relaxed text-gray-900">
            ¿Ya tenés una cuenta?
            <RouterLink to="/login">
              <a
                class="font-bold text-gray-700 ml-2 rounded-lg transition duration-300 hover:bg-indigo-50 focus:bg-indigo-100 p-2"
              >
                Iniciar sesión
              </a>
            </RouterLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>
