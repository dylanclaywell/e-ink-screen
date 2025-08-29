<template>
  <tr class="border-b border-gray-300">
    <td>
      <input v-model="name" class="" type="text" />
    </td>
    <td class="">
      <select v-model="type" class="">
        <option value="literal">Literal</option>
        <option value="object">Object</option>
        <option value="array">Array</option>
        <option value="array-of-objects">Array of Objects</option>
      </select>
    </td>
    <td class="">
      <input v-if="type === 'literal'" v-model="value" class="" type="text" />
      <div v-if="type === 'object' || type === 'array-of-objects'" class="my-4">
        <config-table
          :rows="value as ConfigRow[]"
          @add-row="
            () =>
              (value as ConfigRow[]).push({
                name: '',
                value: '',
                type: 'literal',
              })
          "
          @remove-row="(index) => (value as ConfigRow[]).splice(index, 1)"
        />
      </div>
    </td>
    <td>
      <button
        v-if="showRemoveButton"
        class="w-10 h-10 flex justify-center items-center bg-red-600 hover:bg-red-700 text-white rounded mx-auto"
        @click="$emit('remove')"
      >
        <Icon name="material-symbols:delete" />
      </button>
    </td>
  </tr>
</template>

<script lang="ts" setup>
import type { ConfigRow } from '~~/types/Config'

type Props = {
  showRemoveButton: boolean
}

type Emits = {
  remove: () => void
}

defineProps<Props>()
defineEmits<Emits>()

const name = defineModel<string>('name')
const value = defineModel<string | ConfigRow[] | string[]>('value')
const type = defineModel<string>('type')

watch(
  () => type.value,
  (newType) => {
    if (newType === 'literal') {
      value.value = ''
    } else if (newType === 'object') {
      value.value = [
        {
          name: '',
          value: '',
          type: 'literal',
        },
      ]
    } else if (newType === 'array') {
      value.value = ['']
    } else if (newType === 'array-of-objects') {
      value.value = [
        {
          name: '',
          value: '',
          type: 'literal',
        },
      ]
    }
  },
)
</script>
