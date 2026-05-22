<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const animals = ref([])
const activeIndex = ref(0)
const selectedAnimal = ref(null)
const selectedBetAnimalId = ref('')
const balance = ref(1000)
const bet = ref(50)
const isSpinning = ref(false)
const message = ref('请选择下注动物和投注金额后开始')
const history = ref([])

let spinTimer = 0

const canStart = computed(() => {
  return (
    animals.value.length > 0 &&
    !isSpinning.value &&
    selectedBetAnimalId.value &&
    bet.value > 0 &&
    bet.value <= balance.value
  )
})

const activeAnimal = computed(() => {
  return animals.value[activeIndex.value] ?? null
})

const selectedBetAnimal = computed(() => {
  return animals.value.find((animal) => animal.id === selectedBetAnimalId.value) ?? null
})

const totalWeight = computed(() => {
  return animals.value.reduce((sum, animal) => sum + animal.weight, 0)
})

function winRate(animal) {
  if (!animal || totalWeight.value === 0) {
    return '0.0'
  }

  return ((animal.weight / totalWeight.value) * 100).toFixed(1)
}

function setBet(value) {
  if (isSpinning.value) {
    return
  }
  bet.value = Math.min(value, balance.value)
}

function selectBetAnimal(animal) {
  if (isSpinning.value) {
    return
  }

  selectedBetAnimalId.value = animal.id
  message.value = `已选择${animal.name}，赔率 ${animal.multiplier}x`
}

function normalizeBet() {
  const value = Number(bet.value)
  if (!Number.isFinite(value)) {
    bet.value = 1
    return
  }

  bet.value = Math.max(1, Math.min(Math.floor(value), balance.value, 1000))
}

function stepReel(delay = 72) {
  window.clearInterval(spinTimer)
  spinTimer = window.setInterval(() => {
    activeIndex.value = (activeIndex.value + 1) % animals.value.length
  }, delay)
}

function landOn(data) {
  const result = data.result
  const targetIndex = animals.value.findIndex((animal) => animal.id === result.id)
  const rounds = animals.value.length * 3
  const current = activeIndex.value
  const offset = (targetIndex - current + animals.value.length) % animals.value.length
  const totalSteps = rounds + offset
  let steps = 0

  window.clearInterval(spinTimer)

  const slowDown = () => {
    if (steps >= totalSteps) {
      window.clearTimeout(spinTimer)
      activeIndex.value = targetIndex
      selectedAnimal.value = result
      isSpinning.value = false
      balance.value += data.win
      message.value = data.hit
        ? `开出${result.name}，命中${data.selected.name}，获得 ${data.win} 金币`
        : `开出${result.name}，未命中${data.selected.name}，本轮未中奖`
      history.value.unshift({
        id: `${Date.now()}-${result.id}`,
        selectedName: data.selected.name,
        resultName: result.name,
        bet: bet.value,
        win: data.win,
        hit: data.hit,
        multiplier: data.selected.multiplier,
      })
      history.value = history.value.slice(0, 6)
      return
    }

    activeIndex.value = (activeIndex.value + 1) % animals.value.length
    steps += 1
    const progress = steps / Math.max(totalSteps, 1)
    const delay = 58 + Math.round(progress * progress * 170)
    spinTimer = window.setTimeout(slowDown, delay)
  }

  slowDown()
}

async function startSpin() {
  if (!canStart.value) {
    if (!selectedBetAnimalId.value) {
      message.value = '请先选择下注动物'
    } else if (bet.value > balance.value) {
      message.value = '余额不足，请降低投注金额'
    } else {
      message.value = '请输入有效投注金额'
    }
    return
  }

  normalizeBet()
  isSpinning.value = true
  selectedAnimal.value = null
  balance.value -= bet.value
  message.value = `${selectedBetAnimal.value.name} 已下注，转盘正在滚动`
  stepReel()

  try {
    const response = await fetch('/api/spin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bet: bet.value, animalId: selectedBetAnimalId.value }),
    })

    if (!response.ok) {
      throw new Error(await response.text())
    }

    const data = await response.json()
    window.setTimeout(() => landOn(data), 900)
  } catch (error) {
    window.clearInterval(spinTimer)
    isSpinning.value = false
    balance.value += bet.value
    message.value = `开奖失败：${error.message || '服务不可用'}`
  }
}

async function loadAnimals() {
  try {
    const response = await fetch('/api/animals')
    animals.value = await response.json()
  } catch {
    message.value = '动物奖池加载失败，请确认 Go 服务已启动'
  }
}

onMounted(loadAnimals)

onUnmounted(() => {
  window.clearInterval(spinTimer)
  window.clearTimeout(spinTimer)
})
</script>

<template>
  <main class="app-shell">
    <section class="machine" aria-label="动物老虎机">
      <header class="machine-header">
        <div>
          <p class="eyebrow">Go + Vue</p>
          <h1>动物老虎机</h1>
        </div>
        <div class="balance">
          <span>余额</span>
          <strong>{{ balance }}</strong>
        </div>
      </header>

      <div class="reel-window" :class="{ spinning: isSpinning }">
        <button
          v-for="(animal, index) in animals"
          :key="animal.id"
          type="button"
          class="animal-card"
          :class="{
            active: index === activeIndex,
            winner: selectedAnimal?.id === animal.id,
            selected: selectedBetAnimalId === animal.id,
          }"
          :style="{ '--animal-color': animal.color }"
          :aria-label="`下注${animal.name}，赔率${animal.multiplier}倍`"
          :aria-pressed="selectedBetAnimalId === animal.id"
          :disabled="isSpinning"
          @click="selectBetAnimal(animal)"
        >
          <img :src="animal.icon" :alt="animal.name" />
          <span>{{ animal.name }}</span>
          <strong>{{ animal.multiplier }}x</strong>
          <em v-if="selectedBetAnimalId === animal.id">已下注</em>
        </button>
      </div>

      <div class="status-panel">
        <div>
          <span>当前指针</span>
          <strong>{{ activeAnimal?.name || '--' }}</strong>
        </div>
        <div>
          <span>下注动物</span>
          <strong>{{ selectedBetAnimal?.name || '--' }}</strong>
        </div>
        <p>{{ message }}</p>
      </div>

      <div class="controls">
        <label class="bet-field">
          <span>投注</span>
          <input
            v-model.number="bet"
            type="number"
            min="1"
            max="1000"
            step="10"
            :disabled="isSpinning"
            @blur="normalizeBet"
          />
        </label>

        <div class="quick-bets" aria-label="快捷投注">
          <button type="button" :disabled="isSpinning" @click="setBet(20)">20</button>
          <button type="button" :disabled="isSpinning" @click="setBet(50)">50</button>
          <button type="button" :disabled="isSpinning" @click="setBet(100)">100</button>
          <button type="button" :disabled="isSpinning" @click="setBet(200)">200</button>
        </div>

        <button class="start-button" type="button" :disabled="!canStart" @click="startSpin">
          {{ isSpinning ? '开奖中' : '开始' }}
        </button>
      </div>
    </section>

    <aside class="side-panel">
      <section class="odds-board" aria-label="中奖赔率">
        <h2>中奖赔率</h2>
        <div class="odds-list">
          <article
            v-for="animal in animals"
            :key="animal.id"
            class="odds-row"
            :style="{ '--animal-color': animal.color }"
          >
            <img :src="animal.icon" :alt="animal.name" />
            <div>
              <strong>{{ animal.name }}</strong>
              <span>概率约 {{ winRate(animal) }}%</span>
            </div>
            <b>{{ animal.multiplier }}x</b>
          </article>
        </div>
      </section>

      <section class="history-board" aria-label="开奖记录">
        <h2>开奖记录</h2>
        <div v-if="history.length" class="history-list">
          <article v-for="item in history" :key="item.id" class="history-row">
            <span>{{ item.selectedName }} -> {{ item.resultName }}</span>
            <strong>{{ item.multiplier }}x</strong>
            <b :class="{ lost: !item.hit }">{{ item.hit ? `+${item.win}` : `-${item.bet}` }}</b>
          </article>
        </div>
        <p v-else class="empty-state">暂无记录</p>
      </section>
    </aside>
  </main>
</template>
