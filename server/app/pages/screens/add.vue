<template>
  <div>
    <h1 class="text-2xl mb-4">Add Screen</h1>
    <form>
      <input
        name="name"
        type="text"
        placeholder="Screen Name"
        class="mb-4 p-2 border"
      />
      <div
        ref="canvasContainerRef"
        class="w-full border relative overflow-hidden"
      >
        <div class="toolbar flex gap-4 p-2 bg-gray-100">
          <label>
            Cursor Size:
            <input
              v-model="cursorSize"
              type="number"
              class="p-2 border"
              min="1"
              max="50"
              @keydown.enter.prevent
            />
          </label>
          <button
            :class="[
              'p-2 rounded flex items-center gap-2 hover:bg-gray-200',
              {
                'bg-gray-300 hover:bg-gray-400': cursorType === 'square',
              },
            ]"
            title="Square Cursor"
            type="button"
            @click="() => setCursorType('square')"
          >
            <Icon name="mdi-square" />
          </button>
          <button
            :class="[
              'p-2 rounded flex items-center gap-2 hover:bg-gray-200',
              {
                'bg-gray-300 hover:bg-gray-400': cursorType === 'circle',
              },
            ]"
            title="Circle Cursor"
            type="button"
            @click="() => setCursorType('circle')"
          >
            <Icon name="mdi-circle" />
          </button>
        </div>
        <canvas ref="canvasRef"></canvas>
        <div
          class="absolute bottom-0 left-0 bg-gray-800 text-white text-sm px-2 py-1"
        >
          Position: {{ cursorPosition.x }}, {{ cursorPosition.y }}
        </div>
      </div>
      <div class="flex gap-2 mt-4">
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">
          Save
        </button>
        <NuxtLink to="/" class="px-4 py-2 bg-gray-300 rounded">Cancel</NuxtLink>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvasContainerRef = ref<HTMLDivElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)

const gridWidth = 250
const gridHeight = 120
const zoomLevel = ref(1)
const panOffset = ref({ x: 0, y: 0 })
const isDrawing = ref(false)
const isErasing = ref(false)
const lastPanPosition = ref({ x: 0, y: 0 })
const gridData: (string | null)[][] = Array.from({ length: gridWidth }, () =>
  Array(gridHeight).fill(null),
)
const cursorPosition = ref({ x: 0, y: 0 })
const cursorSize = ref(5)
const cursorType = ref<'square' | 'circle'>('square')

function setCursorType(type: 'square' | 'circle') {
  cursorType.value = type
}

function resizeCanvas() {
  if (canvasContainerRef.value && canvasRef.value) {
    const canvas = canvasRef.value
    const containerWidth = canvasContainerRef.value.offsetWidth
    const containerHeight = containerWidth * (gridHeight / gridWidth)

    canvas.width = containerWidth
    canvas.height = containerHeight

    drawCanvas()
  }
}

function drawCanvas() {
  if (!canvasRef.value) return

  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const pixelWidth = (canvas.width / gridWidth) * zoomLevel.value
  const pixelHeight = (canvas.height / gridHeight) * zoomLevel.value

  ctx.save()
  ctx.translate(panOffset.value.x, panOffset.value.y)

  for (let x = 0; x < gridWidth; x++) {
    for (let y = 0; y < gridHeight; y++) {
      if (gridData[x]?.[y]) {
        ctx.fillStyle = gridData[x]?.[y] || '#fff'
        ctx.fillRect(x * pixelWidth, y * pixelHeight, pixelWidth, pixelHeight)
      }
    }
  }

  ctx.strokeStyle = '#e0e0e0'
  for (let x = 0; x <= gridWidth; x++) {
    ctx.beginPath()
    ctx.moveTo(x * pixelWidth, 0)
    ctx.lineTo(x * pixelWidth, gridHeight * pixelHeight)
    ctx.stroke()
  }
  for (let y = 0; y <= gridHeight; y++) {
    ctx.beginPath()
    ctx.moveTo(0, y * pixelHeight)
    ctx.lineTo(gridWidth * pixelWidth, y * pixelHeight)
    ctx.stroke()
  }

  ctx.restore()
}

function getCanvasCoordinates(event: MouseEvent) {
  if (!canvasRef.value) return { x: 0, y: 0 }
  const rect = canvasRef.value.getBoundingClientRect()
  return {
    x: (event.clientX - rect.left - panOffset.value.x) / zoomLevel.value,
    y: (event.clientY - rect.top - panOffset.value.y) / zoomLevel.value,
  }
}

function startDrawing(event: MouseEvent) {
  if (event.button === 0) isDrawing.value = true
  if (event.button === 2) isErasing.value = true

  const { x, y } = getCanvasCoordinates(event)
  const gridX = Math.floor(x / (canvasRef.value!.width / gridWidth))
  const gridY = Math.floor(y / (canvasRef.value!.height / gridHeight))

  if (
    gridX >= 0 &&
    gridX < gridWidth &&
    gridY >= 0 &&
    gridY < gridHeight &&
    gridData[gridX]
  ) {
    const size = cursorSize.value
    for (let dx = -Math.floor(size / 2); dx <= Math.floor(size / 2); dx++) {
      for (let dy = -Math.floor(size / 2); dy <= Math.floor(size / 2); dy++) {
        const nx = gridX + dx
        const ny = gridY + dy
        if (
          nx >= 0 &&
          nx < gridWidth &&
          ny >= 0 &&
          ny < gridHeight &&
          gridData[nx]
        ) {
          if (
            cursorType.value === 'circle' &&
            dx * dx + dy * dy > (size / 2) * (size / 2)
          ) {
            continue
          }
          gridData[nx][ny] = isDrawing.value ? '#000000' : null
        }
      }
    }
    drawCanvas()
  }

  lastPanPosition.value = { x: gridX, y: gridY }
}

function draw(event: MouseEvent) {
  if (!isDrawing.value && !isErasing.value) return

  const { x, y } = getCanvasCoordinates(event)
  const gridX = Math.floor(x / (canvasRef.value!.width / gridWidth))
  const gridY = Math.floor(y / (canvasRef.value!.height / gridHeight))

  if (gridX < 0 || gridX >= gridWidth || gridY < 0 || gridY >= gridHeight)
    return

  const lastX = lastPanPosition.value.x
  const lastY = lastPanPosition.value.y
  const steps = Math.max(Math.abs(gridX - lastX), Math.abs(gridY - lastY))

  for (let i = 0; i <= steps; i++) {
    const interpolatedX = Math.round(lastX + (gridX - lastX) * (i / steps))
    const interpolatedY = Math.round(lastY + (gridY - lastY) * (i / steps))

    if (
      interpolatedX >= 0 &&
      interpolatedX < gridWidth &&
      interpolatedY >= 0 &&
      interpolatedY < gridHeight &&
      gridData[interpolatedX]
    ) {
      const size = cursorSize.value
      for (let dx = -Math.floor(size / 2); dx <= Math.floor(size / 2); dx++) {
        for (let dy = -Math.floor(size / 2); dy <= Math.floor(size / 2); dy++) {
          const nx = interpolatedX + dx
          const ny = interpolatedY + dy
          if (
            nx >= 0 &&
            nx < gridWidth &&
            ny >= 0 &&
            ny < gridHeight &&
            gridData[nx]
          ) {
            if (
              cursorType.value === 'circle' &&
              dx * dx + dy * dy > (size / 2) * (size / 2)
            ) {
              continue
            }
            gridData[nx][ny] = isDrawing.value ? '#000000' : null
          }
        }
      }
    }
  }

  lastPanPosition.value = { x: gridX, y: gridY }
  drawCanvas()
}

function stopDrawing() {
  isDrawing.value = false
  isErasing.value = false
}

function handleZoom(event: WheelEvent) {
  event.preventDefault()
  const zoomFactor = 0.1
  zoomLevel.value = Math.min(
    Math.max(zoomLevel.value - event.deltaY * zoomFactor * 0.01, 0.5),
    3,
  )
  drawCanvas()
}

function startPanning(event: MouseEvent) {
  event.preventDefault()
  if (event.button !== 1) return
  lastPanPosition.value = { x: event.clientX, y: event.clientY }
  if (canvasRef.value) {
    canvasRef.value.style.cursor = 'grabbing'
  }
}

function pan(event: MouseEvent) {
  if (event.buttons !== 4) return

  const deltaX = event.clientX - lastPanPosition.value.x
  const deltaY = event.clientY - lastPanPosition.value.y

  panOffset.value.x += deltaX
  panOffset.value.y += deltaY

  lastPanPosition.value = { x: event.clientX, y: event.clientY }
  drawCanvas()
}

function stopPanning() {
  if (canvasRef.value) {
    canvasRef.value.style.cursor = 'crosshair'
  }
}

function updateCursorPosition(event: MouseEvent) {
  const { x, y } = getCanvasCoordinates(event)
  cursorPosition.value = {
    x: Math.floor(x / (canvasRef.value!.width / gridWidth)),
    y: Math.floor(y / (canvasRef.value!.height / gridHeight)),
  }
}

function preventContextMenu(event: MouseEvent) {
  event.preventDefault()
}

onMounted(() => {
  resizeCanvas()

  if (canvasRef.value) {
    canvasRef.value.addEventListener('mousedown', startDrawing)
    canvasRef.value.addEventListener('mousemove', draw)
    canvasRef.value.addEventListener('mouseup', stopDrawing)
    canvasRef.value.addEventListener('mouseleave', stopDrawing)
    canvasRef.value.addEventListener('wheel', handleZoom)
    canvasRef.value.addEventListener('contextmenu', preventContextMenu)
    canvasRef.value.addEventListener('mousedown', startPanning)
    canvasRef.value.addEventListener('mousemove', updateCursorPosition)
    window.addEventListener('mousemove', pan)
    window.addEventListener('mouseup', stopDrawing)
    window.addEventListener('mouseup', stopPanning)
  }

  window.addEventListener('resize', resizeCanvas)
})

onUnmounted(() => {
  if (canvasRef.value) {
    canvasRef.value.removeEventListener('mousedown', startDrawing)
    canvasRef.value.removeEventListener('mousemove', draw)
    canvasRef.value.removeEventListener('mouseup', stopDrawing)
    canvasRef.value.removeEventListener('mouseleave', stopDrawing)
    canvasRef.value.removeEventListener('wheel', handleZoom)
    canvasRef.value.removeEventListener('contextmenu', preventContextMenu)
    canvasRef.value.removeEventListener('mousedown', startPanning)
    canvasRef.value.removeEventListener('mousemove', updateCursorPosition)
    window.removeEventListener('mousemove', pan)
    window.removeEventListener('mouseup', stopDrawing)
    window.removeEventListener('mouseup', stopPanning)
  }

  window.removeEventListener('resize', resizeCanvas)
})
</script>

<style scoped>
canvas {
  display: block;
  background-color: #fff;
  cursor: crosshair;
}

.toolbar {
  display: flex;
  align-items: center;
}
</style>
