<template>
  <div>
    <h1 class="text-2xl">Add Config</h1>
    <config-table :rows="rows" @add-row="addRow" @remove-row="removeRow" />
  </div>
</template>

<script lang="ts" setup>
import type { ConfigRow } from '~~/types/Config'

const rows = ref<ConfigRow[]>([{ name: '', value: '', type: 'literal' }])

function addRow() {
  rows.value.push({ name: '', value: '', type: 'literal' })
}

function removeRow(index: number) {
  rows.value.splice(index, 1)
}
</script>
