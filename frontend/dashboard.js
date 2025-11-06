async function fetchJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json();
}

async function loadStats() {
  const s = await fetchJSON('/api/stats');
  document.getElementById('stats').innerHTML = `
    <ul>
      <li>Temp: <strong>${s.means.temperature}</strong> °C</li>
      <li>Pression: <strong>${s.means.pressure}</strong> bar</li>
      <li>Débit: <strong>${s.means.flow}</strong> L/min</li>
      <li>Rendement: <strong>${s.means.yield}</strong> %</li>
      <li>Observations totales: ${s.count}</li>
    </ul>`;

  document.getElementById('last').innerHTML = `
    <ul>
      <li>Temp: <strong>${s.last.temperature}</strong> °C</li>
      <li>Pression: <strong>${s.last.pressure}</strong> bar</li>
      <li>Débit: <strong>${s.last.flow}</strong> L/min</li>
      <li>Rendement: <strong>${s.last.yield}</strong> %</li>
    </ul>`;
}

async function doPredict() {
  const p = await fetchJSON('/api/predict');
  document.getElementById('predOut').textContent = JSON.stringify(p, null, 2);
}

document.getElementById('btnPredict').addEventListener('click', doPredict);

// Petit graphique sur la température en temps réel (polling)
let chart;
async function initChart() {
  const ctx = document.getElementById('tempChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Température (°C)', data: [] }] },
    options: { animation: false, scales: { y: { beginAtZero: false } } }
  });
}

async function tick() {
  try {
    const s = await fetchJSON('/api/stats');
    const label = new Date().toLocaleTimeString();
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(s.last.temperature);
    if (chart.data.labels.length > 50) { chart.data.labels.shift(); chart.data.datasets[0].data.shift(); }
    chart.update();
  } catch (e) { /* ignore */ }
}

(async function() {
  await initChart();
  await loadStats();
  setInterval(loadStats, 5000);
  setInterval(tick, 1000);
})();
