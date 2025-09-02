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
        <div class="toolbar bg-gray-100 py-4">
          <div
            v-if="toolType === 'pencil'"
            class="border-r flex gap-4 px-4 items-center"
          >
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
                'p-2 rounded flex items-center hover:bg-gray-200 w-8 h-8',
                {
                  'bg-gray-300 hover:bg-gray-400': pencilType === 'square',
                },
              ]"
              title="Square Cursor"
              type="button"
              @click="() => setPencilType('square')"
            >
              <Icon name="mdi-square" />
            </button>
            <button
              :class="[
                'p-2 rounded flex items-center hover:bg-gray-200 w-8 h-8',
                {
                  'bg-gray-300 hover:bg-gray-400': pencilType === 'circle',
                },
              ]"
              title="Circle Cursor"
              type="button"
              @click="() => setPencilType('circle')"
            >
              <Icon name="mdi-circle" />
            </button>
          </div>
          <div
            v-if="toolType === 'text'"
            class="border-r flex gap-4 px-4 items-center"
          >
            <label>
              Font:
              <select>
                <option>Arial</option>
              </select>
            </label>
            <label class="ml-2">
              Size:
              <input
                v-model.number="fontSize"
                type="number"
                min="6"
                max="72"
                class="p-1 border rounded w-16 ml-1"
                style="width: 60px"
              />
            </label>
            <label class="ml-4">
              <input
                ref="fontInputRef"
                type="file"
                accept=".ttf,.otf,.woff,.woff2"
                style="display: none"
                @change="handleFontUpload"
              />
              <button
                type="button"
                class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                @click="() => fontInputRef?.click()"
              >
                Upload Font
              </button>
            </label>
          </div>
          <div class="border-r flex gap-4 px-4 items-center">
            <button
              :class="[
                'p-2 rounded flex items-center hover:bg-gray-200 w-8 h-8',
                {
                  'bg-gray-300 hover:bg-gray-400': toolType === 'pencil',
                },
              ]"
              title="Pencil"
              type="button"
              @click="() => setToolType('pencil')"
            >
              <Icon name="mdi-pencil" />
            </button>
            <button
              :class="[
                'p-2 rounded flex items-center hover:bg-gray-200 w-8 h-8',
                {
                  'bg-gray-300 hover:bg-gray-400': toolType === 'text',
                },
              ]"
              title="Add Text"
              type="button"
              @click="() => setToolType('text')"
            >
              <Icon name="mdi-format-letter-case" />
            </button>
          </div>
        </div>
        <canvas ref="canvasRef" />
        <!-- Text input dialog -->
        <div
          v-if="showTextDialog"
          :style="{
            position: 'absolute',
            left: textDialogPosition.x + 'px',
            top: textDialogPosition.y + 'px',
            zIndex: 10,
            background: 'white',
            border: '1px solid #ccc',
            padding: '4px',
            borderRadius: '4px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }"
        >
          <input
            ref="textInputRef"
            v-model="currentTextInput"
            class="p-1 border rounded"
            style="min-width: 100px"
            placeholder="Type text..."
            autofocus
            @input="updateTextOnCanvas"
            @keydown.enter.prevent="commitText"
            @blur="commitText"
          />
        </div>
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
// Font size state
const fontSize = ref(10)
// Text tool state
const showTextDialog = ref(false)
const textDialogPosition = ref({ x: 0, y: 0 })
const textInputRef = ref<HTMLInputElement | null>(null)
const currentTextInput = ref('')
const textCanvasPosition = ref({ x: 0, y: 0 })
// Removed unused textElements
// Helper to convert canvas click to DOM position
function getDomPositionFromCanvas(event: MouseEvent) {
  if (!canvasRef.value) return { x: 0, y: 0 }
  const rect = canvasRef.value.getBoundingClientRect()
  return {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top,
  }
}

function handleCanvasClickForText(event: MouseEvent) {
  // skip anything except left clicks
  if (event.button !== 0) return

  if (toolType.value !== 'text') return
  // Show dialog at click position
  const domPos = getDomPositionFromCanvas(event)
  textDialogPosition.value = domPos
  // Save canvas coordinates for text placement
  const canvasCoords = getCanvasCoordinates(event)
  textCanvasPosition.value = {
    x: Math.floor(canvasCoords.x / (canvasRef.value!.width / gridWidth)),
    y: Math.floor(canvasCoords.y / (canvasRef.value!.height / gridHeight)),
  }
  currentTextInput.value = ''
  showTextDialog.value = true
  nextTick(() => {
    textInputRef.value?.focus()
  })
}

function updateTextOnCanvas() {
  drawCanvas()
}

// Rasterize text to gridData
function rasterizeTextToGrid(text: string, gridX: number, gridY: number) {
  // Create offscreen canvas matching grid size
  const offCanvas = document.createElement('canvas')
  offCanvas.width = gridWidth
  offCanvas.height = gridHeight
  const ctx = offCanvas.getContext('2d')!
  ctx.clearRect(0, 0, gridWidth, gridHeight)
  ctx.font = `bold ${fontSize.value}px Arial` // Use selected font size
  ctx.textBaseline = 'top'
  // Draw text at grid position
  ctx.fillStyle = '#000'
  ctx.fillText(text, gridX, gridY)
  // Read pixel data
  const imageData = ctx.getImageData(0, 0, gridWidth, gridHeight)
  for (let x = 0; x < gridWidth; x++) {
    for (let y = 0; y < gridHeight; y++) {
      const idx = (y * gridWidth + x) * 4
      const alpha = imageData.data[idx + 3]
      // If pixel is not transparent, set gridData
      if ((alpha ?? 0) > 128) {
        gridData[x]![y] = '#000000'
      }
    }
  }
}

function commitText() {
  if (currentTextInput.value.trim() !== '') {
    // Rasterize text into gridData
    rasterizeTextToGrid(
      currentTextInput.value,
      textCanvasPosition.value.x,
      textCanvasPosition.value.y,
    )
    // Optionally, still keep textElements for preview, or remove if not needed
    // textElements.value.push({
    //   x: textCanvasPosition.value.x,
    //   y: textCanvasPosition.value.y,
    //   text: currentTextInput.value,
    // })
  }
  showTextDialog.value = false
  currentTextInput.value = ''
  drawCanvas()
}

const canvasContainerRef = ref<HTMLDivElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const fontInputRef = ref<HTMLInputElement | null>(null)

function handleFontUpload(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    if (file) {
      // You can handle the font file here (e.g., upload to server, load locally, etc.)
      // For now, just log the file name
      console.log('Font uploaded:', file.name)
    }
  }
}

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
const pencilType = ref<'square' | 'circle'>('square')
const toolType = ref<'pencil' | 'text'>('pencil')

function setPencilType(type: 'square' | 'circle') {
  pencilType.value = type
}

function setToolType(type: 'pencil' | 'text') {
  toolType.value = type
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

  // Draw gridData (committed pixels)
  for (let x = 0; x < gridWidth; x++) {
    for (let y = 0; y < gridHeight; y++) {
      if (gridData[x]?.[y]) {
        ctx.fillStyle = gridData[x]?.[y] || '#fff'
        ctx.fillRect(x * pixelWidth, y * pixelHeight, pixelWidth, pixelHeight)
      }
    }
  }

  // Rasterize preview text if dialog is open
  if (showTextDialog.value && currentTextInput.value) {
    // Create a temp grid
    const previewGrid: (string | null)[][] = Array.from(
      { length: gridWidth },
      () => Array(gridHeight).fill(null),
    )
    // Rasterize preview text into previewGrid
    // (reuse rasterizeTextToGrid logic, but write to previewGrid instead of gridData)
    const offCanvas = document.createElement('canvas')
    offCanvas.width = gridWidth
    offCanvas.height = gridHeight
    const offCtx = offCanvas.getContext('2d')!
    offCtx.clearRect(0, 0, gridWidth, gridHeight)
    offCtx.font = `bold ${fontSize.value}px Arial`
    offCtx.textBaseline = 'top'
    offCtx.fillStyle = '#000'
    offCtx.fillText(
      currentTextInput.value,
      textCanvasPosition.value.x,
      textCanvasPosition.value.y,
    )
    const imageData = offCtx.getImageData(0, 0, gridWidth, gridHeight)
    for (let x = 0; x < gridWidth; x++) {
      for (let y = 0; y < gridHeight; y++) {
        const idx = (y * gridWidth + x) * 4
        const alpha = imageData.data?.[idx + 3]
        if (typeof alpha === 'number' && alpha > 128 && previewGrid[x]) {
          previewGrid[x]![y] = '#000000'
        }
      }
    }
    // Draw previewGrid on top
    for (let x = 0; x < gridWidth; x++) {
      for (let y = 0; y < gridHeight; y++) {
        if (Array.isArray(previewGrid[x]) && previewGrid[x]![y]) {
          ctx.fillStyle = previewGrid[x]![y] ?? '#fff'
          ctx.fillRect(x * pixelWidth, y * pixelHeight, pixelWidth, pixelHeight)
        }
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
            pencilType.value === 'circle' &&
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
              pencilType.value === 'circle' &&
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

function handleMouseDown(event: MouseEvent) {
  if (toolType.value === 'text') {
    handleCanvasClickForText(event)
  } else {
    startDrawing(event)
  }
}

function handleKeyDown(event: KeyboardEvent) {
  if (event.key === 'Escape' && showTextDialog.value) {
    showTextDialog.value = false
    currentTextInput.value = ''
    drawCanvas()
  }
}

onMounted(() => {
  resizeCanvas()

  if (canvasRef.value) {
    canvasRef.value.addEventListener('mousedown', handleMouseDown)
    canvasRef.value.addEventListener('mousemove', draw)
    canvasRef.value.addEventListener('mouseup', stopDrawing)
    canvasRef.value.addEventListener('mouseleave', stopDrawing)
    canvasRef.value.addEventListener('wheel', handleZoom)
    canvasRef.value.addEventListener('contextmenu', preventContextMenu)
    canvasRef.value.addEventListener('mousedown', startPanning)
    canvasRef.value.addEventListener('mousemove', updateCursorPosition)
  }

  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('mousemove', pan)
  window.addEventListener('mouseup', stopDrawing)
  window.addEventListener('mouseup', stopPanning)
  window.addEventListener('resize', resizeCanvas)
})

onUnmounted(() => {
  if (canvasRef.value) {
    canvasRef.value.removeEventListener('mousedown', handleMouseDown)
    canvasRef.value.removeEventListener('mousemove', draw)
    canvasRef.value.removeEventListener('mouseup', stopDrawing)
    canvasRef.value.removeEventListener('mouseleave', stopDrawing)
    canvasRef.value.removeEventListener('wheel', handleZoom)
    canvasRef.value.removeEventListener('contextmenu', preventContextMenu)
    canvasRef.value.removeEventListener('mousedown', startPanning)
    canvasRef.value.removeEventListener('mousemove', updateCursorPosition)
  }

  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('mousemove', pan)
  window.removeEventListener('mouseup', stopDrawing)
  window.removeEventListener('mouseup', stopPanning)
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
