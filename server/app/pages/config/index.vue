<template>
  <div>
    <h1 class="text-2xl">Configs</h1>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Last Updated At</th>
          <th class="invisible">Edit</th>
          <th class="invisible">Delete</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td>{{ row.name }}</td>
          <td>{{ row.updatedAt }}</td>
          <td><NuxtLink :to="`/config/edit/${row.name}`">Edit</NuxtLink></td>
          <td>
            <button>Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
const { data } = await useFetch('/api/config')
</script>
