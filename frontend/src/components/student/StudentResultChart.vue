<script setup>
import { init, use } from 'echarts/core'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  AriaComponent,
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

use([
  AriaComponent,
  BarChart,
  CanvasRenderer,
  GridComponent,
  LegendComponent,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
])

const props = defineProps({
  option: { type: Object, required: true },
  label: { type: String, required: true },
  height: { type: Number, default: 300 },
})

const chartElement = ref(null)
let chart
let resizeObserver

function resizeChart() {
  chart?.resize()
}

onMounted(() => {
  chart = init(chartElement.value)
  chart.setOption(props.option)
  if ('ResizeObserver' in window) {
    resizeObserver = new ResizeObserver(resizeChart)
    resizeObserver.observe(chartElement.value)
  }
  window.addEventListener('resize', resizeChart)
})

watch(() => props.option, (option) => chart?.setOption(option, true), { deep: true })

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  window.removeEventListener('resize', resizeChart)
  chart?.dispose()
  chart = undefined
})
</script>

<template>
  <div ref="chartElement" class="min-w-0 w-full" :style="{ height: `${height}px` }" role="img" :aria-label="label"></div>
</template>
