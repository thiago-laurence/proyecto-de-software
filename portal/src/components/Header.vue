
import { isTemplateNode } from '@vue/compiler-core';
<script>
import ItemMenu from './ItemMenu.vue'
import { useUserStore } from '@/stores/user';

export default {
    name: 'Header',
    components: {
        ItemMenu
    },
    setup() {
    const user = useUserStore();

    return {
      user,
    };
  },
    data() {
        return {
            items: [
                { text: 'HOME', link: '/' },
                { text: 'SERVICIOS', link: '/search-services' },
                { text: 'MIS PEDIDOS', link: '/service-orders' },
                { text: 'ESTADÍSTICAS', link: '/stadistics' },
            ],
            isMobileMenuOpen: false,
        }
    },
    methods: {
        toggleMobileMenu() {
            this.isMobileMenuOpen = !this.isMobileMenuOpen;
        },
    },
}

</script>
<template>
    <header>
        <div class="wrapper">
            <nav class="lg:px-4 pt-6 bg-white fixed w-full z-20 top-0 left-0 border-b border-gray-200">
                <div class="w-full flex lg:flex-row flex-wrap justify-between ">
                    <div class="flex place-content-center pb-4 pt-2 px-4 lg:px-0 border-gray-100">
                        <a href="https://cidepint.ing.unlp.edu.ar/" class="flex ml-2">
                            <img src="../assets/img/cidepint-logo.png" class="h-8 mr-3" alt="CIDEPINT Logo" />
                            <span
                                class="self-center text-xl font-normal sm:text-2xl whitespace-nowrap lg:hover:text-blue-700">
                                CIDEPINT
                            </span>
                        </a>
                    </div>
                    <button @click="toggleMobileMenu"
                        class="block lg:hidden px-4 text-black hover:text-gray-200 focus:outline-none">
                        <svg class="h-6 w-6 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <path fill-rule="evenodd"
                                d="M21 4H3a1 1 0 010-2h18a1 1 0 010 2zM21 10H3a1 1 0 110-2h18a1 1 0 010 2zM21 16H3a1 1 0 110-2h18a1 1 0 010 2z">
                            </path>
                        </svg>
                    </button>

                    <div :class="{ 'hidden': !isMobileMenuOpen, 'flex': isMobileMenuOpen }"
                        class="w-full max-lg:flex-col items-center max-lg:border-t max-lg:pt-5 border-gray-100 lg:flex lg:w-auto"
                        id="navbar-sticky">

                        <div class="">
                            <ItemMenu :items="items" class="max-lg:mb-4"></ItemMenu>
                        </div>

                        
                    </div>

                    <div :class="{ 'hidden': !isMobileMenuOpen, 'flex': isMobileMenuOpen }"
                        class="flex max-md:flex-col max-lg:flex-row max-lg:w-full max-lg:place-content-center items-center lg:flex lg:w-auto">
                        <RouterLink to="/login" >
                            <button 
                            v-if="!user.isLoggedIn"
                            class="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800">
                            <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
                                <a class="text-md">
                                Iniciar sesión
                            </a>
                            </span>
                            </button>
                        </RouterLink>

                        <RouterLink v-if="!user.isLoggedIn" to="/sign-up">
                            <button class="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800">
                                <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
                                    <a class="text-md">
                                        Registrarse
                                    </a>
                                </span>
                            </button>
                        </RouterLink>
                        <button v-else @click="user.logout()" class="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800">
                            <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
                                <a class="text-md">
                                    Cerrar sesión
                                </a>
                            </span>
                        </button>
                            
                    </div>
                </div>
            </nav>
        </div>
    </header>
</template>
