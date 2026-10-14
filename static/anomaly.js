'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const asText = (tag, value) => {
    const node = document.createElement(tag);
    node.textContent = String(value ?? '');
    return node;
  };
  const allowed = /^events\/anomaly-\d{6}\.json$/;
  async function load(path) {
    const response = await fetch(path, {cache: 'no-store'});
    if (!response.ok) throw new Error('archive unavailable');
    return response.json();
  }
  async function setup() {
    const status = $('anomaly-status');
    const list = $('anomaly-list');
    if (!status || !list) return;
    try {
      const manifest = await load('anomaly/manifest.json');
      if (manifest.schema_version !== 'dna.anomaly-genesis.v1' || !Array.isArray(manifest.entries)) {
        throw new Error('unrecognized archive format');
      }
      $('anomaly-total').textContent = String(manifest.entries.length);
      list.replaceChildren();
      if (!manifest.entries.length) {
        status.textContent = 'No qualifying structural anomalies recorded yet.';
        return;
      }
      status.textContent = 'Measurements, not verified discoveries. Inspect evidence before drawing conclusions.';
      for (const item of manifest.entries.slice(-6).reverse()) {
        if (!allowed.test(item.path)) continue;
        const button = asText('button', item.detector.replaceAll('_', ' ') + ' / ' + item.detected_at.slice(0, 10));
        button.className = 'chapter-select';
        button.type = 'button';
        button.addEventListener('click', async () => {
          try {
            const event = await load('anomaly/' + item.path);
            const view = $('anomaly-detail');
            view.replaceChildren(asText('strong', event.id + ': ' + event.detector),
                                 asText('p', event.explanation),
                                 asText('p', 'Status: detected, not independently verified. Fictional writing prompt: ' + event.creative_prompt));
            const proof = asText('p', 'Evidence files: ' + (event.evidence || []).map(e => e.path).join('; '));
            view.append(proof);
          } catch (error) {
            $('anomaly-detail').textContent = 'Evidence unavailable: ' + error.message;
          }
        });
        list.append(button);
      }
    } catch (error) {
      status.textContent = 'Anomaly archive unavailable; existing chapters remain readable.';
    }
  }
  setup();
})();
