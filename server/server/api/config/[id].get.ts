import fs from 'fs'
import { parse } from 'yaml'
import type { ConfigRow } from '../../../types/Config'

function parseConfig(config: unknown): ConfigRow[] {
  const rows: ConfigRow[] = []

  if (typeof config !== 'object' || config === null) {
    return rows
  }

  for (const [key, value] of Object.entries(config)) {
    if (Array.isArray(value)) {
      if (value.length === 0) {
        rows.push({ name: key, value: [], type: 'array' })
      } else if (typeof value[0] === 'object' && value[0] !== null) {
        rows.push({
          name: key,
          value: value.flatMap((v) => parseConfig(v)),
          type: 'array-of-objects',
        })
      } else {
        rows.push({ name: key, value: value as string[], type: 'array' })
      }
    } else if (typeof value === 'object' && value !== null) {
      rows.push({
        name: key,
        value: parseConfig(value),
        type: 'object',
      })
    } else {
      rows.push({ name: key, value: String(value), type: 'literal' })
    }
  }

  return rows
}

export default defineEventHandler(async (event) => {
  const { id } = getRouterParams(event)

  const filePath = `./server/data/configs/${id}.yaml`
  if (!fs.existsSync(filePath)) {
    return createError({ statusCode: 404, statusMessage: 'Config not found' })
  }

  const file = fs.readFileSync(filePath, 'utf-8')

  const parsed = parse(file)

  return parseConfig(parsed)
})
