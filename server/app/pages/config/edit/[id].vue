<template>
  <div>
    <h1 class="text-2xl">Edit Config</h1>
    <config-table
      v-if="rows"
      :rows="rows"
      @add-row="addRow"
      @remove-row="removeRow"
    />
    <div class="flex justify-end">
      <button
        class="mt-4 rounded bg-blue-500 hover:bg-blue-600 px-4 py-2 text-white"
      >
        Save
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { ConfigRow } from '~~/types/Config'

const { data: rows } = await useFetch<ConfigRow[]>(
  '/api/config/' + useRoute().params.id,
)

function addRow() {
  rows.value?.push({ name: '', value: '', type: 'literal' })
}

function removeRow(index: number) {
  rows.value?.splice(index, 1)
}
</script>
