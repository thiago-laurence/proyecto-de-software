<template>
    <ul
        class="flex flex-col text-center  w-full items-center  md:p-0 mt-4 font-medium rounded-lg md:flex-row md:space-x-8 md:mt-0 md:border-0 md:bg-white">
        <li v-for="(item, index) in items" :key="index">
            <a href="#"
                class="block py-2 pl-3 pr-4 text-gray-900 rounded  md:hover:bg-transparent hover:text-blue-700 md:p-0 ">
            <RouterLink :to="item.link" class="text-md">{{ item.text }}</RouterLink>
            </a>
        </li>
        
    </ul>
</template>

<script>
export default {
    props: {
        items: Array
    }
}

</script>

<style scoped>

a.router-link-exact-active {
  color: var(--color-text);
}

a.router-link-exact-active:hover {
  background-color: transparent;
}

a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

a:first-of-type {
  border: 0;
}
</style>