<template>
    <div  v-if="order" class=" mx-auto mt-40">
        <div >
            <div class="col-span-1">
                <div class="w-full md:px-10 items-start justify-start mt-10 grid grid-cols-8">
                    <h3 class=" col-span-7 text-5xl font-extrabold dark:text-white">Notas de pedido {{ order.title }}</h3>
                    <div class="flex justify-center m-5">
                    </div>
                </div>
                <br>
                <div class="h-1 w-full bg-indigo-500 rounded"></div>
            </div>

            <div class=" mt-10 h-96">
                <div >
                    <div v-for="comment in order.comments" >
                        <div v-if="comment.user.username != user" class="p-4 my-4 rounded flex flex-col  text-indigo-800 bg-indigo-100 m-5">
                            <span>
                                <svg class="flex-shrink-0 inline w-4 h-4 mr-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm-9 9a9 9 0 0 1 18 0h-2a7 7 0 0 0-14 0H3Z"/>
                                </svg>
                                {{comment.user.username}}
                            </span>
                            <span class="mb-2">{{ comment.comment }}</span>
                        </div> 
                        <div v-if="comment.user.username == user" class="p-4 my-4 rounded flex flex-col text-green-600 bg-green-100 m-5">
                            <span>
                                <svg class="flex-shrink-0 inline w-4 h-4 mr-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm-9 9a9 9 0 0 1 18 0h-2a7 7 0 0 0-14 0H3Z"/>
                                </svg>
                                {{comment.user.username}}
                            </span>
                            <span class="mb-2">{{ comment.comment }}</span>
                        </div>
                    </div>
                </div>
                <p id="aviso" v-if="order.comments.length == 0" class="text-center text-gray-500 dark:text-white mt-20">Aún no hay mensajes</p>
                <form  @submit.prevent="sendMessage">
                    <div class="mb-4 border border-gray-900 rounded-lg bg-gray-50 dark:bg-gray-700 m-5">
                        <div class="px-4 py-2 bg-white rounded-t-lg">
                            <label for="#comment" class="sr-only">Your comment</label>
                            <textarea v-model="comment" id="comment" rows="4" class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400" placeholder="Escribe un comentario..." required></textarea>
                        </div>
                        <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
                            <button type="submit" class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800">
                                Enviar
                            </button>
                            <div class="flex ps-0 space-x-1 rtl:space-x-reverse sm:ps-2">
                                <button type="button" class="inline-flex justify-center items-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600">
                                    <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 12 20">
                                            <path stroke="currentColor" stroke-linejoin="round" stroke-width="2" d="M1 6v8a5 5 0 1 0 10 0V4.5a3.5 3.5 0 1 0-7 0V13a2 2 0 0 0 4 0V6"/>
                                        </svg>
                                    <span class="sr-only">Attach file</span>
                                </button>
                                <button type="button" class="inline-flex justify-center items-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600">
                                    <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 20">
                                            <path d="M8 0a7.992 7.992 0 0 0-6.583 12.535 1 1 0 0 0 .12.183l.12.146c.112.145.227.285.326.4l5.245 6.374a1 1 0 0 0 1.545-.003l5.092-6.205c.206-.222.4-.455.578-.7l.127-.155a.934.934 0 0 0 .122-.192A8.001 8.001 0 0 0 8 0Zm0 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>
                                        </svg>
                                    <span class="sr-only">Set location</span>
                                </button>
                                <button type="button" class="inline-flex justify-center items-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600">
                                    <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                            <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                                        </svg>
                                    <span class="sr-only">Upload image</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </form>

            </div>
        </div>
    </div>
</template>

<script>
    import { API } from '@/api';
    import { useUserStore } from '@/stores/user'

    export default {
        setup(){
            let user = useUserStore();
            user = user.data.username;
            return {
                user
            };
        },
        data() {
            return {
                order: null,
                comment: null
            };
        },
        methods: {
            async sendMessage(){
                if(this.comment == null || this.comment == ''){
                    return;
                }
                const id = this.$route.params.id; // Accede al parámetro id de la URL actual
                await API.post('/me/requests/' + id + '/notes', {
                    comment: this.comment
                })
                .then(response => {
                    this.comment = '';
                    return response.data;
                })
                .catch(error => {
                    console.error('Error al cargar el servicio:', error);
                });

                this.searchComments();
            },
            async searchComments(){
                const id = this.$route.params.id; // Accede al parámetro id de la URL actual    
                await API.get('/me/requests/' + id)
                .then(response => {
                    this.order = response.data;
                })
                .catch(error => {
                    console.error('Error al cargar el servicio:', error);
                });
            }
        },
        async mounted() {
            this.searchComments();
        }
    };

</script>