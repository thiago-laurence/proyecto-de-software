
<template>

    <div class="max-w-lg p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        <div class="h-full flex items-start">
            <div class="flex-grow pl-6">
                
                <h2 class="tracking-widest text-base title-font font-medium text-indigo-500 mb-1 mt-2">
                    <slot name="status"></slot>
                </h2>
                <h1 class="title-font text-xl font-medium text-gray-900 mb-3">
                    <slot name="title"></slot>
                </h1>
                <h2 class="title-font text-base font-medium text-gray-700 mb-3">
                    <slot name="creation_date"></slot>
                    |
                    <slot name="close_date"></slot>
                </h2>
                <p class="leading-relaxed mb-5">
                    <slot name="description"></slot>
                </p>
                <a href="#" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    <slot name="route"></slot>
                    <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                    </svg>
                </a>

            </div>
        </div>
    </div>
</template>

