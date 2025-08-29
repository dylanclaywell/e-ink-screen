import fs from 'fs'

export default defineEventHandler(async () => {
  const configFiles = fs
    .readdirSync('./server/data/configs')
    .filter((file) => file.endsWith('.yaml'))

  return configFiles.map((file) => {
    const name = file.replace('.yaml', '')
    return { id: name, name, updatedAt: new Date() }
  })
})
