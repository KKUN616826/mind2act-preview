/* One public table model for the homepage and full leaderboard. */
(() => {
  const board = document.querySelector('.view-leaderboard');
  if (!board) return;
  const data = JSON.parse(board.querySelector('#viewLeaderboardData').textContent);
  const views = new Map(data.views.map(view => [view.key, view]));
  const tabs = [...board.querySelectorAll('[data-board-view]')];
  const paradigm = board.querySelector('#board-paradigm');
  const search = board.querySelector('#model-search');
  const difficulty = board.querySelector('#board-difficulty');
  const rows = [...board.querySelectorAll('tbody tr')];
  const models = new Map(data.models.map(model => [model.id, model]));
  const frame = document.querySelector('.lunar-worlds-frame');
  const fullLink = document.querySelector('.full-leader-link a');
  const standalone = !frame;
  let sceneReady = !!frame?.contentDocument?.querySelector('#scene');
  const query = new URLSearchParams(location.search);
  let view = views.has(query.get('view')) ? query.get('view') : 'mind';
  if (Object.hasOwn(data.paradigms, query.get('paradigm'))) paradigm.value = query.get('paradigm');
  search.value = query.get('q') || '';
  if (['all','easy','medium','hard'].includes(query.get('difficulty'))) difficulty.value=query.get('difficulty');

  function notifyScene() {
    frame?.contentWindow?.postMessage({type: 'mind2act-select-world', world: view}, location.origin);
  }
  function render() {
    const current = views.get(view);
    board.dataset.view = view;
    tabs.forEach(tab => {
      const selected = tab.dataset.boardView === view;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    board.querySelector('#board-panel').setAttribute('aria-labelledby', `board-tab-${view}`);
    board.querySelector('#board-title').textContent = current.label;
    board.querySelector('#board-description').textContent = current.description;
    board.querySelector('caption').textContent = `${current.label} leaderboard · ${difficulty.value==='all'?'All-level results':difficulty.value+' · TBD'}`;
    const q = search.value.trim().toLocaleLowerCase();
    let count = 0, reported = 0;
    const ranked=data.models.filter(m=>m.results[view]?.score!=null).sort((a,b)=>b.results[view].score-a.results[view].score);
    const ordered=[...ranked,...data.models.filter(m=>m.results[view]?.score==null)];
    const tbody=board.querySelector('tbody');
    ordered.forEach(m=>tbody.append(rows.find(r=>r.dataset.modelId===m.id)));
    board.querySelector('.board-status').textContent=difficulty.value==='all'?'All-level results':'Breakdown pending';
    rows.forEach(row => {
      const model = models.get(row.dataset.modelId);
      row.hidden = !(paradigm.value === 'all' || model.paradigm === paradigm.value) || !model.name.toLocaleLowerCase().includes(q);
      if (!row.hidden) count++;
      const result=model.results[view], aggregate=difficulty.value==='all';
      if(!row.hidden&&aggregate&&result?.score!=null)reported++;
      row.children[0].textContent=aggregate&&result?.score!=null?String(ranked.findIndex(m=>m.results[view].score===result.score)+1):'—';
      row.children[3].textContent=aggregate?(result?.score==null?'—':result.score.toFixed(2)):'TBD';
      row.children[4].textContent=aggregate?(result?.success==null?'—':result.success.toFixed(1)):'TBD';
      row.children[3].classList.toggle('score-value',aggregate&&result?.score!=null);
      row.children[4].classList.toggle('pending-value',!aggregate);
      row.children[3].classList.toggle('pending-value',!aggregate);
    });
    board.querySelector('.board-count').textContent = `${count} models · ${data.paradigms[paradigm.value] || 'All paradigms'} · ${difficulty.value==='all'?reported+' reported':'Difficulty breakdown pending'}`;
    board.querySelector('.board-empty').hidden = count !== 0;
    const tasks = current.tasks.map(task => {
      const link = document.createElement('a');
      link.href = `tasks/${task}.html`;
      link.textContent = task;
      return link;
    });
    board.querySelector('.board-task-links').replaceChildren(...tasks);
    const params = new URLSearchParams({view});
    if (paradigm.value !== 'all') params.set('paradigm', paradigm.value);
    if (search.value) params.set('q', search.value);
    if(difficulty.value!=='all')params.set('difficulty',difficulty.value);
    if (fullLink) fullLink.href = `leaderboard.html?${params}`;
    if (standalone) {
      const url = new URL(location.href);
      for (const key of ['view', 'paradigm', 'q', 'difficulty']) url.searchParams.delete(key);
      for (const [key, value] of params) url.searchParams.set(key, value);
      history.replaceState(null, '', url);
    }
  }
  function select(key) {
    if (!views.has(key)) return;
    view = key;
    render();
    notifyScene();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(tab.dataset.boardView));
    tab.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
      tabs[next].focus();
      select(tabs[next].dataset.boardView);
    });
  });
  paradigm.addEventListener('change', render);
  search.addEventListener('input', render);
  difficulty.addEventListener('change',render);
  frame?.addEventListener('load', () => { sceneReady = true; notifyScene(); });
  window.addEventListener('message', event => {
    if (!frame || !sceneReady || event.origin !== location.origin || event.source !== frame.contentWindow) return;
    if (event.data?.type === 'mind2act-world' && views.has(event.data.world)) {
      view = event.data.world;
      render();
    }
  });
  render();
  notifyScene();
})();
