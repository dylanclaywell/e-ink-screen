<template>
  <table>
    <thead>
      <tr>
        <th class="text-left">Name</th>
        <th class="text-left">Type</th>
        <th class="text-left">Value</th>
        <th class="invisible">Add New</th>
      </tr>
    </thead>
    <tbody>
      <config-row
        v-for="(row, index) in rows"
        :key="index"
        v-model:name="row.name"
        v-model:value="row.value"
        v-model:type="row.type"
        :show-remove-button="rows.length > 1"
        @remove="$emit('removeRow', index)"
      />
    </tbody>
  </table>
  <button class="mt-4 button--primary" @click="$emit('addRow')">Add Row</button>
</template>

<script lang="ts" setup>
import type { ConfigRow } from '~~/types/Config'

type Props = {
  rows: ConfigRow[]
}

type Emits = {
  addRow: []
  removeRow: [index: number]
}

defineProps<Props>()
defineEmits<Emits>()
</script>
