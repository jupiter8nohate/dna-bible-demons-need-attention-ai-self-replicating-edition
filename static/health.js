'use strict';
(async () => {
  const view = document.getElementById('operational-status');
  if (!view) return;
  try {
    const response = await fetch('health/status.json', {cache: 'no-store'});
    if (!response.ok) throw Error('Status missing');
    const status = await response.json();
    view.textContent = status.status.toUpperCase() + ' | ' + status.chapters +
      ' chapters | ' + status.anomaly_records + ' anomalies | ' +
      (status.last_prose_mode || 'no prose') + ' | last: ' + (status.last_chapter_at || 'none');
    const age = Date.now() - Date.parse(status.last_chapter_at);
    if (status.status !== 'operational' || !Number.isFinite(age) || age > 10800000) {
      view.textContent += ' | STALE: inspect GitHub Actions';
    }
  } catch {
    view.textContent = 'Status unavailable. Check GitHub Actions before assuming publication continues.';
  }
})();