<script>
    export default {
        name: 'TextImg',
        props: {
            direction: String,
            text: String,
            icon: String
        }
    }
</script>

<template>
    <section :class="['flex', direction , 'lg:h-60', 'w-full', 'border-2', 'border-indigo-200', 'rounded-md','card', 'max-lg:flex-col', 'max-lg:pb-5']" >
        <div class="flex max-lg:flex-row  lg:flex-col justify-center lg:pl-20 items-center lg:mr-5 w-1/10 max-lg:px-2 max-lg:mt-3">
          <span class="material-symbols-outlined max-lg:text-center text-3xl lg:px-10 lg:text-6xl">
          {{  icon }}
        </span>
        </div>
        <div class="flex max-lg:flex-row lg:flex-col justify-center items-center max-lg:px-2 max-lg:mt-3 lg:px-10 w-9/10 ">
          <div class="lg:text-2xl text-md max-lg:text-center text-gray-100 font-light lg:py-5">
            {{ text }}
          </div>
        </div>
      </section>
</template>
<style>
.card {
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.9)), url('../assets/img/fondo2.jpg');
  background-repeat: repeat-y;
}
</style>

