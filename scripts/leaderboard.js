// Tables are pre-rendered so the candidate roster remains readable offline.
const lbPanels = [...document.querySelectorAll('[data-lb-panel]')];
const lbButtons = [...document.querySelectorAll('[data-lb-track]')];
let lbTrack = 'vla';
function updateLeaderboard() {
  const view = document.getElementById('leaderboardView').value;
  const query = document.getElementById('leaderboardSearch').value.trim().toLocaleLowerCase();
  let count = 0;
  for (const panel of lbPanels) {
    const active = panel.dataset.track === lbTrack && panel.dataset.view === view;
    panel.hidden = !active;
    for (const row of panel.querySelectorAll('[data-lb-row]')) {
      row.hidden = !row.dataset.name.includes(query);
      if (active && !row.hidden) count++;
    }
  }
  lbButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lbTrack === lbTrack)));
  document.getElementById('leaderboardStatus').textContent = (lbTrack === 'vla' ? 'VLA / WAM' : 'Coding Agent') + ' · ' + count + ' 个候选 · 全部待评测 · 不按性能排序';
  document.getElementById('leaderboardEmpty').hidden = count !== 0;
}
lbButtons.forEach(button => button.addEventListener('click', () => { lbTrack = button.dataset.lbTrack; updateLeaderboard(); }));
document.getElementById('leaderboardView').addEventListener('change', updateLeaderboard);
document.getElementById('leaderboardSearch').addEventListener('input', updateLeaderboard);
window.addEventListener('beforeprint', () => lbPanels.forEach(panel => panel.hidden = false));
window.addEventListener('afterprint', updateLeaderboard);
document.querySelector('.lb-download').addEventListener('click', event => {
  event.preventDefault();
  const data = JSON.parse(document.getElementById('leaderboardData').textContent);
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], {type:'application/json;charset=utf-8'}));
  const link = document.createElement('a');
  link.href = url; link.download = 'leaderboard.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
updateLeaderboard();
