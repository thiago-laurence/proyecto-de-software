<template>
    <div v-if="show" :class="notificationClasses">
      <div>
        <svg class="flex-shrink-0 inline w-4 h-4 mr-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <span >{{ message }}</span>
      </div>  
      <button @click="close" class="ml-2font-semibold focus:outline-none" fill="currentColor">
        Cerrar
      </button>
    </div>
</template>
  
<script>
  export default {
    props: {
      type: {
        type: String,
        required: true,
      },
      message: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        show: true,
      };
    },
    computed: {
      notificationClasses() {
        return [
          'notification',
          this.type,
        ];
      },
    },
    methods: {
      close() {
        this.show = false;
      },
    },
  };
</script>
  
<style scoped>
  .notification {
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 0.25rem;
    display: flex;
    justify-content: space-between;

    padding: 1rem;
    font-size: 0.875rem/* 14px */;
    line-height: 1.25rem;

    --tw-text-opacity: 1;
    --tw-bg-opacity: 1;
  }
  
  .info {
    color: rgb(30 64 175 / var(--tw-text-opacity));
    background-color: rgb(239 246 255 / var(--tw-bg-opacity));
  }
  
  .success {  
    color: rgb(22 101 52 / var(--tw-text-opacity));
    background-color: rgb(240 253 244 / var(--tw-bg-opacity));
  }
  
  .warning {
    color: rgb(133 77 14 / var(--tw-text-opacity));
    background-color: rgb(254 252 232 / var(--tw-bg-opacity));
  }
  
  .error {
    color: rgb(153 27 27 / var(--tw-text-opacity));
    background-color: rgb(254 242 242 / var(--tw-bg-opacity));
  }
</style>
  