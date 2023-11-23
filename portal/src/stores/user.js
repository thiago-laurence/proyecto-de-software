import { API } from '@/api'
import { defineStore } from "pinia"

export const useUserStore = defineStore({
    'id': 'user',
    state: () => {
        return {
            data: {},
            isLogged: false
        }
    },
    persist: {
        key: 'user',
        storage: localStorage,
    },
    getters: {
        isLoggedIn: (state) => state.isLogged,
    },
    actions: {
        logout(){
            this.$patch({
                data: '',
                isLogged: false 
            });
            localStorage.removeItem('jwt');
            localStorage.removeItem('user');
            window.location.href = '/';
        },
        async login(email, password){
            await API.post('/auth/', {email, password})
            .then(response => {
                const data = response.data.token;
                localStorage.setItem('jwt', data);
            })
            await API.get('/me/profile')
            .then(({ data }) => {
                this.$patch({
                    data: data,
                    isLogged: true
                });
            })
        },
        async login_google(response){
            await API.post('/auth/verify-token', { token: response.access_token })
            .then(response => {
                const data = response.data.token;
                localStorage.setItem('jwt', data);
            })

            await API.get('/me/profile')
            .then(({ data }) => {
                this.$patch({
                    data: data,
                    isLogged: true
                });
            })
        },
        async sign_up(email, name, lastname){
            const response = await API.post('/auth/sign-up', {email, name, lastname})
            return response;
        },
    }
});