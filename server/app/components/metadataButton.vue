<template>
  <div>
    <button
      :class="[
        'w-full flex justify-between items-center p-2 hover:bg-gray-100',
        { 'bg-gray-100 rounded-t-md': isOpen, 'rounded-md': !isOpen },
      ]"
      @click="isOpen = !isOpen"
    >
      <span class="text-lg">{{ metadata.name }}</span
      ><Icon :name="isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'" />
    </button>
    <div v-show="isOpen" class="bg-gray-100 p-2 rounded-b-md">
      <label class="flex flex-col">
        <span class="text-sm">Name</span>
        <input v-model="metadata.name" class="compact" name="name" />
      </label>
      <label class="flex flex-col">
        <span class="text-sm">Placeholder</span>
        <input
          v-model="metadata.placeholder"
          class="compact"
          name="placeholder"
        />
      </label>
      <div class="flex basis-1/2 gap-2">
        <label class="flex flex-col">
          <span class="text-sm">X</span>
          <input
            v-model="metadata.position.x"
            class="compact w-full"
            name="position.x"
          />
        </label>
        <label class="flex flex-col">
          <span class="text-sm">Y</span>
          <input
            v-model="metadata.position.y"
            class="compact w-full"
            name="position.y"
          />
        </label>
      </div>
      <label class="flex flex-col">
        <span class="text-sm">Alignment</span>
        <select v-model="metadata.alignment" class="compact" name="alignment">
          <option value="left">Left</option>
          <option value="center">Center</option>
        </select>
      </label>
    </div>
  </div>
</template>

<script lang="ts" setup>
const metadata = defineModel<{
  name: string
  placeholder: string
  position: { x: number; y: number }
  alignment: 'left' | 'center'
}>('metadata', {
  default: {
    name: '',
    placeholder: '',
    position: { x: 0, y: 0 },
    alignment: 'left',
  },
})

const isOpen = ref(false)
</script>
