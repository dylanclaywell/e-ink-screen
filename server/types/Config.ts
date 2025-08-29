export type ConfigRowType = 'literal' | 'object' | 'array-of-objects' | 'array'

export type ConfigRow = {
  name: string
  value: string | ConfigRow[] | string[]
  type: ConfigRowType
}
