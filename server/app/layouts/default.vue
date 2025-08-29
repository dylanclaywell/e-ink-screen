<template>
  <div>
    <nav class="max-w-full">
      <div class="flex justify-between items-center p-4 shadow-md">
        <NuxtLink to="/" class="text-4xl">e-Ink</NuxtLink>
        <div class="flex gap-4">
          <NuxtLink to="/config">Configs</NuxtLink>
        </div>
      </div>
    </nav>
    <div class="overflow-auto min-h-[calc(100vh-72px)]">
      <main class="py-8"><slot /></main>
    </div>
  </div>
</template>
