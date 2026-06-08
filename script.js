// ── ESTADO ──
  let treinos    = []
  let exercicios = []
  let metas      = []
  let evolucoes  = []

  const icones = { musculacao: 'ti-barbell', cardio: 'ti-heart-rate-monitor', funcional: 'ti-accessible', corrida: 'ti-run' }
  let selectedTreino = null
  let currentPage    = 'treinos'
  let exFiltro       = null
  let searchTerm     = ''

  // ── API ──
  // Todas as funções que falam com o Flask ficam aqui.
  // GET busca dados, POST cria, DELETE remove.

  async function apiGet(rota) {
    const res = await fetch(rota)
    return res.json()
  }

  async function apiPost(rota, corpo) {
    const res = await fetch(rota, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo)
    })
    return res.json()
  }

  async function apiDelete(rota) {
    const res = await fetch(rota, { method: 'DELETE' })
    return res.json()
  }

  async function apiPut(rota, corpo) {
    const res = await fetch(rota, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo)
    })
    return res.json()
  }

  // ── CARREGAR DADOS DO SERVIDOR ──
  async function carregarTudo() {
    treinos    = await apiGet('/treinos')
    exercicios = await apiGet('/exercicios')
    metas      = await apiGet('/metas')
    evolucoes  = await apiGet('/evolucoes')
    renderTreinos()
  }

  // ── HELPERS ──
  function modoLabel(e) {
    if (e.modo === 'series')    return `${e.series} séries × ${e.repeticoes} reps`
    if (e.modo === 'tempo')     return `${e.tempo}s`
    if (e.modo === 'distancia') return `${e.distancia}m`
  }
  function modoIcon(e) {
    if (e.modo === 'series')    return 'ti-repeat'
    if (e.modo === 'tempo')     return 'ti-clock'
    if (e.modo === 'distancia') return 'ti-map-pin'
  }
  function formatDate(d) {
    if (!d) return '—'
    if (d.includes('/')) return d
    const [y, m, day] = d.split('-')
    return `${day}/${m}/${y}`
  }

  // ── STATS ──
  function updateStats() {
    document.getElementById('s-treinos').textContent    = treinos.length
    document.getElementById('s-exercicios').textContent = exercicios.length
    document.getElementById('s-minutos').textContent    = treinos.reduce((s, t) => s + Number(t.duracao), 0)
  }

  // ── RENDER TREINOS ──
  function renderTreinos() {
    updateStats()
    const term = searchTerm.toLowerCase()
    const list = treinos.filter(t =>
      t.nome.toLowerCase().includes(term) ||
      t.tipo.includes(term) ||
      t.objetivo.toLowerCase().includes(term)
    )
    const el = document.getElementById('treino-list')
    el.innerHTML = list.length ? list.map(t => `
      <div class="treino-card${selectedTreino === t.nome ? ' selected' : ''}" onclick="selectTreino('${t.nome}')">
        <div class="treino-icon icon-${t.tipo}"><i class="ti ${icones[t.tipo] || 'ti-barbell'}"></i></div>
        <div class="treino-info">
          <div class="treino-nome">${t.nome}</div>
          <div class="treino-meta">
            <span><i class="ti ti-calendar"></i>${formatDate(t.data)}</span>
            <span><i class="ti ti-clock"></i>${t.duracao} min</span>
            <span><i class="ti ti-target"></i>${t.objetivo}</span>
          </div>
        </div>
        <span class="badge badge-${t.tipo}">${t.tipo}</span>
        <div class="card-actions">
          <button class="icon-btn del" onclick="event.stopPropagation();confirmDelete('treino','${t.nome}')" aria-label="Excluir"><i class="ti ti-trash"></i></button>
        </div>
      </div>`).join('')
      : `<div class="empty"><i class="ti ti-barbell"></i>Nenhum treino encontrado</div>`
  }

  // ── SELECT TREINO ──
  function selectTreino(nome) {
    selectedTreino = nome
    renderTreinos()
    const exs = exercicios.filter(e => e.treino === nome)
    const t   = treinos.find(t => t.nome === nome)
    document.getElementById('detail-panel').classList.remove('hidden')
    document.getElementById('detail-title').textContent = nome
    document.getElementById('detail-sub').textContent   = `${t.tipo} · ${t.duracao} min`
    document.getElementById('detail-body').innerHTML = exs.length
      ? exs.map(e => `
          <div class="ex-item">
            <div class="ex-nome">${e.nome}</div>
            <div class="ex-modo"><i class="ti ${modoIcon(e)}"></i>${modoLabel(e)}</div>
          </div>`).join('')
      : `<div class="empty" style="padding:1.5rem"><i class="ti ti-run"></i>Nenhum exercício</div>`
  }

  function closeDetail() {
    selectedTreino = null
    document.getElementById('detail-panel').classList.add('hidden')
    renderTreinos()
  }

  // ── RENDER EXERCÍCIOS PAGE ──
  function renderExPage() {
    if (!exFiltro && treinos.length) exFiltro = treinos[0].nome
    const tabs = document.getElementById('ex-tabs')
    tabs.innerHTML = treinos.map(t => `
      <button class="tab${exFiltro === t.nome ? ' active' : ''}" onclick="setExFiltro('${t.nome}')">${t.nome}</button>`).join('')
    const exs = exercicios.filter(e => e.treino === exFiltro)
    document.getElementById('ex-section-label').textContent = `${exs.length} exercício(s) — ${exFiltro || '—'}`
    document.getElementById('ex-list').innerHTML = exs.length
      ? exs.map((e) => `
          <div class="treino-card">
            <div class="treino-icon icon-${treinos.find(t => t.nome === e.treino)?.tipo || 'musculacao'}">
              <i class="ti ${modoIcon(e)}"></i>
            </div>
            <div class="treino-info">
              <div class="treino-nome">${e.nome}</div>
              <div class="treino-meta"><span><i class="ti ${modoIcon(e)}"></i>${modoLabel(e)}</span></div>
            </div>
            <div class="card-actions">
              <button class="icon-btn del" onclick="confirmDelete('ex',${exercicios.indexOf(e)})" aria-label="Excluir"><i class="ti ti-trash"></i></button>
            </div>
          </div>`).join('')
      : `<div class="empty"><i class="ti ti-run"></i>Nenhum exercício nesse treino</div>`
  }

  function setExFiltro(nome) { exFiltro = nome; renderExPage() }

  // ── RENDER METAS PAGE ──
  function renderMetasPage() {
    const el = document.getElementById('metas-list')
    if (!el) return
    el.innerHTML = metas.length ? metas.map((m, i) => `
      <div class="treino-card">
        <div class="treino-icon icon-musculacao"><i class="ti ti-target"></i></div>
        <div class="treino-info">
          <div class="treino-nome">${m.descricao}</div>
          <div class="treino-meta">
            <span><i class="ti ti-calendar"></i>${m.prazo}</span>
            <span><i class="ti ti-circle-check"></i>${m.status}</span>
          </div>
        </div>
        <div class="card-actions">
          <button class="icon-btn del" onclick="confirmDelete('meta',${i})" aria-label="Excluir"><i class="ti ti-trash"></i></button>
        </div>
      </div>`).join('')
      : `<div class="empty"><i class="ti ti-target"></i>Nenhuma meta cadastrada</div>`
  }

  // ── NAVEGAÇÃO ──
  function navTo(page, btn) {
    currentPage = page
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'))
    btn.classList.add('active')
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'))
    document.getElementById('page-' + page).classList.add('active')
    const titles = { treinos: 'Treinos', exercicios: 'Exercícios', metas: 'Metas', evolucao: 'Evolução', sugestoes: 'Sugestões', timer: '⏱️ Timer de Intervalo', config: 'Configurações' }
    document.getElementById('page-title').textContent = titles[page] || page
    document.getElementById('add-btn').style.display = ['sugestoes', 'timer', 'config'].includes(page) ? 'none' : 'inline-flex'
    closeDetail()
    if (page === 'exercicios') renderExPage()
    if (page === 'treinos')    renderTreinos()
    if (page === 'metas')      renderMetasPage()
    if (page === 'evolucao')   renderEvolucaoPage()
  }

  // ── SEARCH ──
  function onSearch() {
    searchTerm = document.getElementById('search-input').value
    if (currentPage === 'treinos') renderTreinos()
  }

  // ── MODAIS ──
  function openModal(id)  { document.getElementById(id).classList.remove('hidden') }
  function closeModal(id) { document.getElementById(id).classList.add('hidden') }

  function openAddModal() {
    if (currentPage === 'exercicios') { openAddExModal(); return }
    if (currentPage === 'metas')      { openAddMetaModal(); return }
    if (currentPage === 'evolucao')   {
      document.getElementById('ev-data').value         = ''
      document.getElementById('ev-peso-input').value   = ''
      document.getElementById('ev-altura-input').value = ''
      document.getElementById('ev-gordura-input').value = ''
      openModal('modal-evolucao'); return
    }
    document.getElementById('f-nome').value     = ''
    document.getElementById('f-duracao').value  = ''
    document.getElementById('f-objetivo').value = ''
    document.getElementById('f-data').value     = ''
    openModal('modal-treino')
  }

  // ── SALVAR TREINO → Flask ──
  async function salvarTreino() {
    const nome = document.getElementById('f-nome').value.trim()
    if (!nome) { alert('Digite um nome para o treino.'); return }
    await apiPost('/treinos', {
      nome,
      tipo:     document.getElementById('f-tipo').value,
      duracao:  parseInt(document.getElementById('f-duracao').value) || 60,
      data:     document.getElementById('f-data').value,
      objetivo: document.getElementById('f-objetivo').value.trim() || '—',
    })
    closeModal('modal-treino')
    treinos = await apiGet('/treinos')
    renderTreinos()
  }

  // ── MODAL EXERCÍCIO ──
  function openAddExModal(treinoNome) {
    const sel = document.getElementById('ex-treino-sel')
    sel.innerHTML = treinos.map(t =>
      `<option value="${t.nome}"${t.nome === (treinoNome || selectedTreino) ? ' selected' : ''}>${t.nome}</option>`
    ).join('')
    document.getElementById('ex-nome').value = ''
    renderExFields()
    openModal('modal-ex')
  }

  function renderExFields() {
    const modo = document.getElementById('ex-modo').value
    const f    = document.getElementById('ex-fields')
    if (modo === 'series')
      f.innerHTML = `<div class="form-row"><div class="form-group"><label class="form-label">Séries</label><input class="form-input" id="ex-v1" type="number" placeholder="4" min="1"/></div><div class="form-group"><label class="form-label">Repetições</label><input class="form-input" id="ex-v2" type="number" placeholder="12" min="1"/></div></div>`
    else if (modo === 'tempo')
      f.innerHTML = `<div class="form-group"><label class="form-label">Tempo (segundos)</label><input class="form-input" id="ex-v1" type="number" placeholder="60" min="1"/></div>`
    else
      f.innerHTML = `<div class="form-group"><label class="form-label">Distância (metros)</label><input class="form-input" id="ex-v1" type="number" placeholder="1000" min="1"/></div>`
  }

  // ── SALVAR EXERCÍCIO → Flask ──
  async function salvarEx() {
    const nome   = document.getElementById('ex-nome').value.trim()
    const treino = document.getElementById('ex-treino-sel').value
    const modo   = document.getElementById('ex-modo').value
    if (!nome) { alert('Digite o nome do exercício.'); return }
    const v1 = parseInt(document.getElementById('ex-v1')?.value) || 0
    const v2 = parseInt(document.getElementById('ex-v2')?.value) || 0
    await apiPost('/exercicios', {
      nome, treino, modo,
      series:     modo === 'series'    ? v1 : 0,
      repeticoes: modo === 'series'    ? v2 : 0,
      tempo:      modo === 'tempo'     ? v1 : 0,
      distancia:  modo === 'distancia' ? v1 : 0
    })
    closeModal('modal-ex')
    exercicios = await apiGet('/exercicios')
    updateStats()
    if (currentPage === 'exercicios') renderExPage()
    if (selectedTreino === treino) selectTreino(treino)
  }

  // ── MODAL META ──
  function openAddMetaModal() {
    document.getElementById('m-descricao').value = ''
    document.getElementById('m-prazo').value     = ''
    openModal('modal-meta')
  }

  async function salvarMeta() {
    const descricao = document.getElementById('m-descricao').value.trim()
    if (!descricao) { alert('Digite a descrição da meta.'); return }
    await apiPost('/metas', {
      descricao,
      prazo:  document.getElementById('m-prazo').value,
      status: 'Em andamento'
    })
    closeModal('modal-meta')
    metas = await apiGet('/metas')
    renderMetasPage()
  }

  // ── CONFIRMAR EXCLUSÃO ──
  function confirmDelete(tipo, id) {
    const msgs = {
      treino:   `Excluir o treino <strong>${id}</strong>? Os exercícios vinculados também serão removidos.`,
      ex:       `Excluir este exercício?`,
      meta:     `Excluir esta meta?`,
      evolucao: `Excluir este registro de evolução?`
    }
    document.getElementById('confirm-msg').innerHTML = msgs[tipo]
    document.getElementById('confirm-ok').onclick = async () => {
      if (tipo === 'treino') {
        await apiDelete(`/treinos/${encodeURIComponent(id)}`)
        treinos    = await apiGet('/treinos')
        exercicios = await apiGet('/exercicios')
        if (selectedTreino === id) closeDetail()
        renderTreinos()
      } else if (tipo === 'ex') {
        await apiDelete(`/exercicios/${id}`)
        exercicios = await apiGet('/exercicios')
        updateStats()
        if (currentPage === 'exercicios') renderExPage()
      } else if (tipo === 'meta') {
        await apiDelete(`/metas/${id}`)
        metas = await apiGet('/metas')
        renderMetasPage()
      } else if (tipo === 'evolucao') {
        await apiDelete(`/evolucoes/${id}`)
        evolucoes = await apiGet('/evolucoes')
        renderEvolucaoPage()
      }
      closeModal('modal-confirm')
    }
    openModal('modal-confirm')
  }

  // ── RENDER EVOLUÇÃO ──
  function renderEvolucaoPage() {
    const el = document.getElementById('evolucao-list')
    if (!el) return

    // Atualiza stats com o registro mais recente
    if (evolucoes.length > 0) {
      const ultimo = evolucoes[evolucoes.length - 1]
      document.getElementById('ev-peso').textContent    = ultimo.peso
      document.getElementById('ev-gordura').textContent = ultimo.gordura
      const imc = (parseFloat(ultimo.peso) / (parseFloat(ultimo.altura) ** 2)).toFixed(1)
      document.getElementById('ev-imc').textContent = isNaN(imc) ? '—' : imc
    }

    el.innerHTML = evolucoes.length ? [...evolucoes].reverse().map((ev, i) => {
      const idx = evolucoes.length - 1 - i
      const imc = (parseFloat(ev.peso) / (parseFloat(ev.altura) ** 2)).toFixed(1)
      return `
        <div class="treino-card">
          <div class="treino-icon icon-funcional"><i class="ti ti-activity"></i></div>
          <div class="treino-info">
            <div class="treino-nome">${ev.data}</div>
            <div class="treino-meta">
              <span><i class="ti ti-weight"></i>${ev.peso} kg</span>
              <span><i class="ti ti-ruler"></i>${ev.altura} m</span>
              <span><i class="ti ti-flame"></i>${ev.gordura}% gordura</span>
              <span><i class="ti ti-activity"></i>IMC: ${isNaN(imc) ? '—' : imc}</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="icon-btn del" onclick="confirmDelete('evolucao',${idx})" aria-label="Excluir"><i class="ti ti-trash"></i></button>
          </div>
        </div>`
    }).join('') : `<div class="empty"><i class="ti ti-chart-line"></i>Nenhum registro ainda</div>`
  }

  async function salvarEvolucao() {
    const data    = document.getElementById('ev-data').value
    const peso    = parseFloat(document.getElementById('ev-peso-input').value)
    const altura  = parseFloat(document.getElementById('ev-altura-input').value)
    const gordura = parseFloat(document.getElementById('ev-gordura-input').value)
    if (!data || !peso || !altura) { alert('Preencha data, peso e altura.'); return }
    await apiPost('/evolucoes', { data, peso, altura, gordura: gordura || 0 })
    closeModal('modal-evolucao')
    evolucoes = await apiGet('/evolucoes')
    renderEvolucaoPage()
  }

  // ── SUGESTÕES ──
  async function buscarSugestoes(tipo, btn) {
    document.querySelectorAll('#page-sugestoes .tab').forEach(t => t.classList.remove('active'))
    btn.classList.add('active')
    const el = document.getElementById('sugestoes-content')
    el.innerHTML = `<div class="empty"><i class="ti ti-loader"></i>Carregando...</div>`
    const s = await apiGet(`/sugestoes?tipo=${tipo}`)
    el.innerHTML = `
      <div class="dica-card">
        <i class="ti ti-bulb"></i>
        <p><strong>Dica do dia:</strong> ${s.dica_geral}</p>
      </div>
      <div class="sugestao-grid">
        <div class="sugestao-card">
          <div class="sugestao-card-title"><i class="ti ti-run"></i>Exercícios sugeridos</div>
          <ul>${s.exercicios.map(e => `<li>${e}</li>`).join('')}</ul>
        </div>
        <div class="sugestao-card">
          <div class="sugestao-card-title"><i class="ti ti-calendar"></i>Divisão semanal</div>
          <p>${s.divisao}</p>
        </div>
        <div class="sugestao-card">
          <div class="sugestao-card-title"><i class="ti ti-zzz"></i>Descanso</div>
          <p>${s.descanso}</p>
        </div>
        <div class="sugestao-card">
          <div class="sugestao-card-title"><i class="ti ti-salad"></i>Alimentação</div>
          <p>${s.alimentacao}</p>
        </div>
      </div>`
  }

  // ══════════════════════════════════════════
  // TIMER DE INTERVALO
  // ══════════════════════════════════════════

  // Estado do timer
  let timerTotal    = 60    // tempo configurado em segundos
  let timerRestante = 60    // tempo restante atual
  let timerInterval = null  // referência ao setInterval — necessário para parar
  let timerRodando  = false // controla se está rodando ou pausado
  let timerInicio   = null  // timestamp de quando o timer foi iniciado
  const CIRCUNFERENCIA = 2 * Math.PI * 96  // ~603px — perímetro do círculo SVG

  // Histórico de intervalos da sessão
  // Cada item: { duracao, completou, hora }
  let timerHistorico = []

  // ── Formatar segundos em MM:SS ──
  function formatarTempo(seg) {
    const m = Math.floor(seg / 60).toString().padStart(2, '0')
    const s = (seg % 60).toString().padStart(2, '0')
    return `${m}:${s}`
  }

  // ── Atualizar o arco SVG do círculo ──
  // O stroke-dashoffset controla quanto do círculo está "preenchido"
  // Quando offset = 0, o círculo está completo (cheio)
  // Quando offset = CIRCUNFERÊNCIA, o círculo está vazio
  function atualizarArco(restante) {
    const progresso = restante / timerTotal
    const offset    = CIRCUNFERENCIA * (1 - progresso)
    const arco      = document.getElementById('timer-arc')
    arco.style.strokeDashoffset = offset

    // Muda a cor conforme o tempo restante
    arco.classList.remove('warning', 'danger')
    if (restante <= 10)                          arco.classList.add('danger')
    else if (restante <= timerTotal * 0.3)       arco.classList.add('warning')
  }

  // ── Atualizar o display de texto ──
  function atualizarDisplay() {
    document.getElementById('timer-display').textContent = formatarTempo(timerRestante)
    atualizarArco(timerRestante)
  }

  // ── Definir um preset de tempo ──
  function setPreset(segundos, btn) {
    if (timerRodando) return  // não muda enquanto está rodando

    // Atualiza visual dos botões
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'))
    btn.classList.add('active')

    // Limpa o input customizado
    document.getElementById('timer-custom-input').value = ''

    timerTotal    = segundos
    timerRestante = segundos
    atualizarDisplay()
    document.getElementById('timer-status-label').textContent = 'pronto'
  }

  // ── Definir tempo personalizado ──
  function setCustomTime(valor) {
    const seg = parseInt(valor)
    if (!seg || seg <= 0) return

    // Remove destaque dos presets
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'))

    timerTotal    = seg
    timerRestante = seg
    atualizarDisplay()
    document.getElementById('timer-status-label').textContent = 'pronto'
  }

  // ── Iniciar ou pausar ──
  function toggleTimer() {
    if (timerRodando) {
      pausarTimer()
    } else {
      iniciarTimer()
    }
  }

  function iniciarTimer() {
    if (timerRestante <= 0) resetTimer()

    timerRodando = true
    timerInicio  = Date.now()

    // Atualiza o botão para "pausar"
    document.getElementById('timer-play-btn').classList.add('running')
    document.getElementById('timer-play-icon').className = 'ti ti-player-pause'
    document.getElementById('timer-status-label').textContent = 'em andamento'

    // setInterval chama a função a cada 1000ms (1 segundo)
    timerInterval = setInterval(() => {
      timerRestante--
      atualizarDisplay()

      if (timerRestante <= 0) {
        // Timer completou — registra no histórico e toca alerta
        clearInterval(timerInterval)
        timerRodando = false
        document.getElementById('timer-play-btn').classList.remove('running')
        document.getElementById('timer-play-icon').className = 'ti ti-player-play'
        document.getElementById('timer-status-label').textContent = 'concluído!'
        atualizarArco(0)

        // Registra no histórico como completo
        registrarHistorico(timerTotal, true)

        // Alerta sonoro e visual
        document.getElementById('timer-display').style.color = 'var(--green)'
        setTimeout(() => {
          document.getElementById('timer-display').style.color = ''
        }, 1500)
      }
    }, 1000)
  }

  function pausarTimer() {
    clearInterval(timerInterval)
    timerRodando = false
    document.getElementById('timer-play-btn').classList.remove('running')
    document.getElementById('timer-play-icon').className = 'ti ti-player-play'
    document.getElementById('timer-status-label').textContent = 'pausado'
  }

  // ── Resetar o timer ──
  function resetTimer() {
    clearInterval(timerInterval)
    timerRodando  = false
    timerRestante = timerTotal

    document.getElementById('timer-play-btn').classList.remove('running')
    document.getElementById('timer-play-icon').className = 'ti ti-player-play'
    document.getElementById('timer-status-label').textContent = 'pronto'
    document.getElementById('timer-display').style.color = ''

    atualizarDisplay()
  }

  // ── Registrar intervalo manualmente (botão bandeira) ──
  function addLapManual() {
    // Calcula quanto tempo passou desde o início
    const decorrido = timerTotal - timerRestante
    if (decorrido <= 0 && !timerRodando) {
      alert('Inicie o timer antes de registrar um intervalo.')
      return
    }
    // Pausa e registra como incompleto (interrompido manualmente)
    if (timerRodando) pausarTimer()
    registrarHistorico(decorrido, false)
    resetTimer()
  }

  // ── Adicionar item ao histórico ──
  function registrarHistorico(duracao, completou) {
    const agora = new Date()
    const hora  = agora.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })

    timerHistorico.unshift({ duracao, completou, hora })  // unshift adiciona no início
    renderHistorico()
  }

  // ── Renderizar o histórico na tela ──
  function renderHistorico() {
    const el = document.getElementById('timer-history')

    if (timerHistorico.length === 0) {
      el.innerHTML = `<div class="empty" style="padding:1rem"><i class="ti ti-clock"></i>Nenhum intervalo registrado ainda</div>`
      return
    }

    el.innerHTML = timerHistorico.map((item, i) => `
      <div class="history-item">
        <div class="history-item-left">
          <i class="ti ti-${item.completou ? 'circle-check' : 'circle-x'}"></i>
          <span>Intervalo ${timerHistorico.length - i} — ${item.hora}</span>
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="history-item-time">${formatarTempo(item.duracao)}</span>
          <span class="history-badge${item.completou ? '' : ' incomplete'}">
            ${item.completou ? 'completo' : 'interrompido'}
          </span>
        </div>
      </div>`).join('')
  }

  // ── Limpar histórico ──
  function clearHistory() {
    timerHistorico = []
    renderHistorico()
  }

  // ── Inicializar o display ao carregar ──
  atualizarDisplay()


  // ══════════════════════════════════════════
  // CONFIGURAÇÕES: TEMA E IDIOMA
  // ══════════════════════════════════════════

  // Strings de interface em PT e EN
  const i18n = {
    pt: {
      nav: { treinos: 'Treinos', exercicios: 'Exercícios', metas: 'Metas', evolucao: 'Evolução', sugestoes: 'Sugestões', timer: '⏱️ Timer de Intervalo', config: 'Configurações' },
      titles: { treinos: 'Treinos', exercicios: 'Exercícios', metas: 'Metas', evolucao: 'Evolução', sugestoes: 'Sugestões', timer: '⏱️ Timer de Intervalo', config: 'Configurações' },
      search: 'Buscar...',
      addBtn: 'Adicionar',
      stats: { treinos: 'Treinos', exercicios: 'Exercícios', minutos: 'Minutos', cadastrados: 'cadastrados', total: 'no total', planejados: 'planejados' },
      sectionTreinos: 'seus treinos',
      emptyTreinos: 'Nenhum treino encontrado',
      emptyExercicios: 'Nenhum exercício nesse treino',
      emptyMetas: 'Nenhuma meta cadastrada',
      emptyEvolucao: 'Nenhum registro ainda',
      detailSub: 'exercícios do treino',
      addExBtn: 'Adicionar exercício',
      modalTreino: { title: 'Adicionar treino', nome: 'Nome do treino', nomePh: 'ex: Treino A', tipo: 'Tipo', duracao: 'Duração (min)', data: 'Data', objetivo: 'Objetivo', objetivoPh: 'ex: Ganhar massa', cancel: 'Cancelar', save: 'Salvar treino' },
      modalEx: { title: 'Adicionar exercício', treino: 'Treino', nome: 'Nome do exercício', nomePh: 'ex: Agachamento', modo: 'Modo de medição', cancel: 'Cancelar', save: 'Salvar exercício' },
      modalEvolucao: { title: 'Registrar evolução física', data: 'Data', peso: 'Peso (kg)', pesoPh: 'ex: 75.5', altura: 'Altura (m)', alturaPh: 'ex: 1.75', gordura: '% de gordura corporal', gorduraPh: 'ex: 18.5', cancel: 'Cancelar', save: 'Salvar' },
      modalMeta: { title: 'Adicionar meta', desc: 'Descrição da meta', descPh: 'ex: Perder 5kg', prazo: 'Prazo (DD/MM/AAAA)', prazoPh: 'ex: 31/12/2025', cancel: 'Cancelar', save: 'Salvar meta' },
      confirmDelete: 'Excluir',
      confirmCancel: 'Cancelar',
      timerStatus: { pronto: 'pronto', andamento: 'em andamento', pausado: 'pausado', concluido: 'concluído!' },
      timerHistory: 'histórico da sessão',
      timerClear: 'Limpar',
      timerNone: 'Nenhum intervalo registrado ainda',
      timerCompleto: 'completo',
      timerInterrompido: 'interrompido',
      timerIntervalo: 'Intervalo',
      modoSeries: 'Séries e repetições', modoTempo: 'Tempo', modoDistancia: 'Distância',
      exSeries: 'Séries', exReps: 'Repetições', exTempo: 'Tempo (segundos)', exDist: 'Distância (metros)',
      sugestoesLabel: 'filtrar por tipo de treino',
      sugestoesEmpty: 'Selecione um tipo acima para ver sugestões',
      sugestoesLoading: 'Carregando...',
      dicaLabel: 'Dica do dia:',
      sugestoesCards: { exercicios: 'Exercícios sugeridos', divisao: 'Divisão semanal', descanso: 'Descanso', alimentacao: 'Alimentação' },
      configAppearance: 'Aparência', configLightTheme: 'Tema claro', configLightDesc: 'Alterna entre fundo escuro e claro',
      configLang: 'Idioma', configLangLabel: 'Idioma da interface', configLangDesc: 'Afeta menus, rótulos e mensagens',
      evPeso: 'Último peso', evGordura: 'Último % gordura', evImc: 'IMC atual',
      evPesoSub: 'kg', evGorduraSub: '%', evImcSub: 'calculado',
      historico: 'histórico',
      metaStatus: { andamento: 'Em andamento', concluida: 'Concluída' },
    },
    en: {
      nav: { treinos: 'Workouts', exercicios: 'Exercises', metas: 'Goals', evolucao: 'Progress', sugestoes: 'Suggestions', timer: '⏱️ Rest Timer', config: 'Settings' },
      titles: { treinos: 'Workouts', exercicios: 'Exercises', metas: 'Goals', evolucao: 'Progress', sugestoes: 'Suggestions', timer: '⏱️ Rest Timer', config: 'Settings' },
      search: 'Search...',
      addBtn: 'Add',
      stats: { treinos: 'Workouts', exercicios: 'Exercises', minutos: 'Minutes', cadastrados: 'registered', total: 'total', planejados: 'planned' },
      sectionTreinos: 'your workouts',
      emptyTreinos: 'No workouts found',
      emptyExercicios: 'No exercises in this workout',
      emptyMetas: 'No goals registered',
      emptyEvolucao: 'No records yet',
      detailSub: 'workout exercises',
      addExBtn: 'Add exercise',
      modalTreino: { title: 'Add workout', nome: 'Workout name', nomePh: 'e.g. Workout A', tipo: 'Type', duracao: 'Duration (min)', data: 'Date', objetivo: 'Goal', objetivoPh: 'e.g. Build muscle', cancel: 'Cancel', save: 'Save workout' },
      modalEx: { title: 'Add exercise', treino: 'Workout', nome: 'Exercise name', nomePh: 'e.g. Squat', modo: 'Measurement mode', cancel: 'Cancel', save: 'Save exercise' },
      modalEvolucao: { title: 'Log physical progress', data: 'Date', peso: 'Weight (kg)', pesoPh: 'e.g. 75.5', altura: 'Height (m)', alturaPh: 'e.g. 1.75', gordura: 'Body fat %', gorduraPh: 'e.g. 18.5', cancel: 'Cancel', save: 'Save' },
      modalMeta: { title: 'Add goal', desc: 'Goal description', descPh: 'e.g. Lose 5kg', prazo: 'Deadline (DD/MM/YYYY)', prazoPh: 'e.g. 31/12/2025', cancel: 'Cancel', save: 'Save goal' },
      confirmDelete: 'Delete',
      confirmCancel: 'Cancel',
      timerStatus: { pronto: 'ready', andamento: 'running', pausado: 'paused', concluido: 'done!' },
      timerHistory: 'session history',
      timerClear: 'Clear',
      timerNone: 'No intervals recorded yet',
      timerCompleto: 'complete',
      timerInterrompido: 'stopped',
      timerIntervalo: 'Interval',
      modoSeries: 'Sets & reps', modoTempo: 'Time', modoDistancia: 'Distance',
      exSeries: 'Sets', exReps: 'Reps', exTempo: 'Time (seconds)', exDist: 'Distance (meters)',
      sugestoesLabel: 'filter by workout type',
      sugestoesEmpty: 'Select a type above to see suggestions',
      sugestoesLoading: 'Loading...',
      dicaLabel: 'Tip of the day:',
      sugestoesCards: { exercicios: 'Suggested exercises', divisao: 'Weekly split', descanso: 'Rest', alimentacao: 'Nutrition' },
      configAppearance: 'Appearance', configLightTheme: 'Light theme', configLightDesc: 'Switch between dark and light background',
      configLang: 'Language', configLangLabel: 'Interface language', configLangDesc: 'Affects menus, labels and messages',
      evPeso: 'Last weight', evGordura: 'Last body fat %', evImc: 'Current BMI',
      evPesoSub: 'kg', evGorduraSub: '%', evImcSub: 'calculated',
      historico: 'history',
      metaStatus: { andamento: 'In progress', concluida: 'Completed' },
    }
  }

  let currentLang = localStorage.getItem('fitplanner-lang') || 'pt'

  function t(key) {
    const keys = key.split('.')
    let val = i18n[currentLang]
    for (const k of keys) val = val?.[k]
    return val ?? key
  }

  function applyLang() {
    const s = i18n[currentLang]
    // Sidebar nav labels
    const navMap = { treinos: 0, exercicios: 1, metas: 2, evolucao: 3, sugestoes: 4, timer: 5, config: 6 }
    const navItems = document.querySelectorAll('.nav-item')
    const navKeys = ['treinos', 'exercicios', 'metas', 'evolucao', 'sugestoes', 'timer', 'config']
    const navIcons = ['ti-barbell', 'ti-run', 'ti-target', 'ti-chart-line', 'ti-bulb', 'ti-stopwatch', 'ti-settings']
    navItems.forEach((el, i) => {
      if (navKeys[i]) el.innerHTML = `<i class="ti ${navIcons[i]}"></i> ${s.nav[navKeys[i]]}`
    })
    // Topbar
    document.getElementById('search-input').placeholder = s.search
    document.getElementById('add-btn').innerHTML = `<i class="ti ti-plus"></i> ${s.addBtn}`
    // Stats
    document.querySelector('#s-treinos').closest('.stat-card').querySelector('.stat-label').innerHTML = `<i class="ti ti-barbell"></i> ${s.stats.treinos}`
    document.querySelector('#s-exercicios').closest('.stat-card').querySelector('.stat-label').innerHTML = `<i class="ti ti-run"></i> ${s.stats.exercicios}`
    document.querySelector('#s-minutos').closest('.stat-card').querySelector('.stat-label').innerHTML = `<i class="ti ti-clock"></i> ${s.stats.minutos}`
    document.querySelectorAll('.stat-sub')[0].textContent = s.stats.cadastrados
    document.querySelectorAll('.stat-sub')[1].textContent = s.stats.total
    document.querySelectorAll('.stat-sub')[2].textContent = s.stats.planejados
    // Detail panel
    document.getElementById('detail-sub').textContent = s.detailSub
    document.querySelector('#detail-panel button.btn-green').innerHTML = `<i class="ti ti-plus"></i> ${s.addExBtn}`
    // Modal treino
    document.querySelector('#modal-treino .modal-title').textContent = s.modalTreino.title
    // Modal exercicio
    document.querySelector('#modal-ex .modal-title').textContent = s.modalEx.title
    // Modal evolucao
    document.querySelector('#modal-evolucao .modal-title').textContent = s.modalEvolucao.title
    // Modal meta
    document.querySelector('#modal-meta .modal-title').textContent = s.modalMeta.title
    // Evolucao stat labels
    document.querySelector('#ev-peso').closest('.stat-card').querySelector('.stat-label').innerHTML = `<i class="ti ti-weight"></i> ${s.evPeso}`
    document.querySelector('#ev-gordura').closest('.stat-card').querySelector('.stat-label').innerHTML = `<i class="ti ti-flame"></i> ${s.evGordura}`
    document.querySelector('#ev-imc').closest('.stat-card').querySelector('.stat-label').innerHTML = `<i class="ti ti-activity"></i> ${s.evImc}`
    document.querySelectorAll('#page-evolucao .stat-sub')[0].textContent = s.evPesoSub
    document.querySelectorAll('#page-evolucao .stat-sub')[1].textContent = s.evGorduraSub
    document.querySelectorAll('#page-evolucao .stat-sub')[2].textContent = s.evImcSub
    // Config page labels
    document.querySelector('.config-section:nth-child(1) .config-section-title').textContent = s.configAppearance
    document.querySelectorAll('.config-row-label')[0].textContent = s.configLightTheme
    document.querySelectorAll('.config-row-desc')[0].textContent = s.configLightDesc
    document.querySelector('.config-section:nth-child(2) .config-section-title').textContent = s.configLang
    document.querySelectorAll('.config-row-label')[1].textContent = s.configLangLabel
    document.querySelectorAll('.config-row-desc')[1].textContent = s.configLangDesc
    // Timer history title
    document.querySelector('.timer-history-title').textContent = s.timerHistory
    document.querySelector('.timer-history-header .btn').innerHTML = `<i class="ti ti-trash"></i> ${s.timerClear}`
    // Timer status (se não estiver rodando)
    if (!timerRodando) {
      const lbl = document.getElementById('timer-status-label')
      if (lbl && (lbl.textContent === i18n.pt.timerStatus.pronto || lbl.textContent === i18n.en.timerStatus.pronto))
        lbl.textContent = s.timerStatus.pronto
    }
    // Page title update
    if (currentPage) {
      document.getElementById('page-title').textContent = s.titles[currentPage] || currentPage
    }
    // Lang buttons
    document.getElementById('lang-pt').classList.toggle('active', currentLang === 'pt')
    document.getElementById('lang-en').classList.toggle('active', currentLang === 'en')
    // Re-render current page to update dynamic content
    if (currentPage === 'treinos')    renderTreinos()
    if (currentPage === 'exercicios') renderExPage()
    if (currentPage === 'metas')      renderMetasPage()
    if (currentPage === 'evolucao')   renderEvolucaoPage()
    if (currentPage === 'timer')      renderHistorico()
  }

  function setLang(lang) {
    currentLang = lang
    localStorage.setItem('fitplanner-lang', lang)
    applyLang()
  }

  function toggleTheme(isLight) {
    document.body.classList.toggle('light', isLight)
    localStorage.setItem('fitplanner-theme', isLight ? 'light' : 'dark')
  }

  // Restaurar preferências salvas
  ;(function restorePrefs() {
    const theme = localStorage.getItem('fitplanner-theme')
    if (theme === 'light') {
      document.body.classList.add('light')
      document.getElementById('toggle-theme').checked = true
    }
    const lang = localStorage.getItem('fitplanner-lang')
    if (lang) currentLang = lang
  })()

  // ── INIT: carrega tudo do Flask ao abrir ──
  carregarTudo().then(() => applyLang())