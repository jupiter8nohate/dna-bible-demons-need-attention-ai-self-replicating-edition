'use strict';
(() => {
  const area = document.getElementById('insight-observatory');
  if (!area) return;
  const byId = id => document.getElementById(id);
  const text = (tag, value) => {
    const element = document.createElement(tag);
    element.textContent = String(value ?? '');
    return element;
  };
  const load = async path => {
    const response = await fetch(path, {cache: 'no-store'});
    if (!response.ok) throw new Error('Unavailable ' + path);
    return response.json();
  };
  (async () => {
    try {
      const [index, manuscript] = await Promise.all([
        load('insights/manifest.json'), load('book/manifest.json')
      ]);
      if (index.schema_version !== 'dna.insight-queue.v1') throw new Error('Unknown record format');
      const rows = Array.isArray(index.entries) ? index.entries.slice(-12).reverse() : [];
      const chapterRows = Array.isArray(manuscript.entries) ? manuscript.entries : [];
      const referenced = new Map();
      // Only the most recent chapters are needed for the bounded public summary.
      await Promise.all(chapterRows.slice(-100).map(async item => {
        try {
          const chapter = await load('book/' + item.path);
          const id = chapter.insight_reference?.id;
          if (id) referenced.set(id, item.id);
        } catch (_) { /* Remain useful if a historical chapter is unavailable. */ }
      }));
      byId('insight-count').textContent = String(index.entries?.length || 0);
      const list = byId('insight-list');
      list.replaceChildren();
      for (const row of rows) {
        if (!/^events\/insight-\d{6}\.json$/.test(row.path)) continue;
        const event = await load('insights/' + row.path);
        const item = document.createElement('div');
        item.className = 'row';
        item.appendChild(text('strong', event.id + ' / ' + (referenced.get(event.id) ? 'Chapter ' + referenced.get(event.id) : 'Research queue')));
        item.appendChild(text('p', event.question));
        item.appendChild(text('small', 'Watch headline metadata / NOT independently verified / ' + (event.boundary_ids || []).join(' + ')));
        let url;
        try {
          const proposed = new URL(event.source_url);
          if (proposed.protocol === 'https:') url = proposed.href;
        } catch (_) { /* Ignore untrusted URLs. */ }
        if (url) {
          const link = text('a', 'Publisher source ↗');
          link.href = url;
          link.rel = 'noopener noreferrer';
          link.target = '_blank';
          item.appendChild(link);
        }
        list.appendChild(item);
      }
      byId('insight-status').textContent = 'Records are source-linked research leads, not fact-check certifications. The book consumes each research lead at most once.';
    } catch (error) {
      byId('insight-status').textContent = 'Insight ledger unavailable: ' + error.message;
    }
  })();
})();
