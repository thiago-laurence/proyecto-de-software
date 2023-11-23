<script>
    export default {
        name: 'InfoIcon',
        props: {
            text: String,
            icon: String
        }
    }
</script>

<template>
    <section :class="['flex', 'w-full', 'rounded-md']" >
        <div class="flex flex-col justify-center items-center  w-1/10">
          <span class="material-symbols-outlined">
          {{  icon }}
        </span>
        </div>
        <div class="flex flex-col justify-center items-center px-5 w-9/10 ">
          <div class=" text-gray-100 font-light drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
            {{ text }}
          </div>
        </div>
      </section>
</template>

