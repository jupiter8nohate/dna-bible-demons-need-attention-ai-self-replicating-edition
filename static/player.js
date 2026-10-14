'use strict';
(() => {
  const byId = id => document.getElementById(id);
  const make = (tag, content, className) => {
    const el = document.createElement(tag);
    if (content != null) el.textContent = content;
    if (className) el.className = className;
    return el;
  };
  const fetchJSON = async path => {
    const r = await fetch(path, {cache: 'no-store'});
    if (!r.ok) throw new Error('Cannot load ' + path + ' (' + r.status + ')');
    return r.json();
  };
  const storageKey = 'dna-interactive-reader-v2';
  const prefsKey = 'dna-interactive-timer-v2';
  const readStore = (key) => { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } };
  const store = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private modes */ } };
  const linkUrl = value => { try { const u = new URL(value); return u.protocol === 'https:' ? u.href : null; } catch {return null;} };
  let manifest = [];
  let graph = null;
  let save = null;
  let selected = null;
  let countdown = null;
  let deadline = 0;
  let remaining = 10000;
  let timed = readStore(prefsKey);
  if (typeof timed !== 'boolean') timed = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function persist() { if (save) store(storageKey, save); }
  function stopClock() { if (countdown) clearInterval(countdown); countdown = null; }
  function renderTimer(seconds) {
    byId('timebar').style.width = (Math.max(0, Math.min(10, seconds))/10*100) + '%';
    byId('remaining').textContent = timed ? (Math.ceil(seconds) + 's') : 'UNTIMED';
  }
  function startClock(options) {
    stopClock();
    const panel = byId('decision-timer');
    panel.hidden = !options.length;
    if (!options.length) return;
    remaining = 10000;
    renderTimer(10);
    if (!timed) return;
    deadline = performance.now() + remaining;
    countdown = setInterval(() => {
      if (document.hidden) { deadline = performance.now() + remaining; return; }
      remaining = Math.max(0, deadline - performance.now());
      renderTimer(remaining / 1000);
      if (remaining <= 0) {
        stopClock();
        take(0, true);
      }
    }, 100);
  }
  function displayState() {
    byId('chapter-number').textContent = 'CHAPTER ' + String(selected.chapter).padStart(6, '0');
    byId('world-name').textContent = graph.world_name;
    byId('reader-path').textContent = 'DECISIONS ' + save.history.length + ' / LOOPS ' + save.loops + ' / MEMORY ' + save.flags.length;
    const choices = byId('choices');
    choices.replaceChildren();
    const scene = graph.scenes[save.scene];
    byId('scene-name').textContent = scene.title;
    byId('scene-body').textContent = scene.body + ((save.visits[save.scene] || 0) > 1 && scene.echo ? '\n\n' + scene.echo : '');
    byId('chapter-meta').textContent = graph.title + ' • ' + graph.date + ' • ' + graph.world_lens;
    byId('memory').textContent = save.flags.length ? 'ECHOES: ' + save.flags.slice(-7).join(' / ') : 'No prior decisions recorded in this reading.';
    const ending = Boolean(scene.ending);
    byId('end-panel').hidden = !ending;
    byId('choice-heading').hidden = ending;
    if (!ending) {
      for (const [i, option] of scene.choices.entries()) {
        const btn = make('button', (i + 1) + '  ' + option.label, 'choice');
        btn.type = 'button';
        btn.onclick = () => take(i, false);
        choices.append(btn);
      }
    }
    startClock(scene.choices);
    byId('back').disabled = !save.history.length;
    byId('next-chapter').disabled = manifest.findIndex(e => e.chapter === selected.chapter) === manifest.length - 1;
    persist();
  }
  function take(optionNumber, auto) {
    const scene = graph.scenes[save.scene];
    const choice = scene?.choices?.[optionNumber];
    if (!choice) return;
    stopClock();
    save.history.push({from: save.scene, label: choice.label, auto: Boolean(auto)});
    if (save.history.length > 1500) save.history.splice(0, 500);
    if (!save.flags.includes(choice.flag)) save.flags.push(choice.flag);
    if (choice.next === graph.start && save.scene !== graph.start) save.loops++;
    save.scene = choice.next;
    save.visits[save.scene] = (save.visits[save.scene] || 0) + 1;
    displayState();
    byId('scene-name').focus();
  }
  async function openChapter(entry, recover = false) {
    stopClock();
    const doc = await fetchJSON('interactive/' + entry.path);
    if (!doc || doc.schema_version !== 'dna.interactive-manuscript.v1' || !doc.scenes || !doc.scenes[doc.start]) {
      throw new Error('Invalid interactive book data');
    }
    graph = doc;
    selected = entry;
    const old = readStore(storageKey);
    const canRestore = recover && old && old.chapter === entry.chapter && doc.scenes[old.scene] && Array.isArray(old.history) && Array.isArray(old.flags) && old.visits;
    save = canRestore ? old : {chapter: entry.chapter, scene: doc.start, visits: {[doc.start]:1}, history: [], loops: 0, flags: []};
    const log = byId('chapter-list');
    log.querySelectorAll('button').forEach(b => b.setAttribute('aria-current', String(b.dataset.id === String(entry.chapter))));
    displayState();
  }
  function reset() { if (!graph || !selected) return; openChapter(selected, false).catch(showError); }
  function rewind() {
    if (!graph || !save || !save.history.length) return;
    const last = save.history.pop();
    stopClock();
    save.scene = last.from;
    save.visits[save.scene] = (save.visits[save.scene] || 0) + 1;
    // Echo flags deliberately survive rewinds: experience changes the observer.
    displayState();
    byId('scene-name').focus();
  }
  function showError(error) { stopClock(); byId('scene-name').textContent = 'Signal interrupted'; byId('scene-body').textContent = String(error); }
  async function setup() {
    byId('timer-toggle').onclick = () => {
      timed = !timed;
      store(prefsKey, timed);
      byId('timer-toggle').textContent = timed ? 'Disable timed choices' : 'Enable timed choices';
      if (graph && save) displayState();
    };
    byId('timer-toggle').textContent = timed ? 'Disable timed choices' : 'Enable timed choices';
    byId('restart').onclick = reset;
    byId('back').onclick = rewind;
    byId('next-chapter').onclick = () => {
      const i = manifest.findIndex(e => e.chapter === selected.chapter);
      if (i >= 0 && i < manifest.length - 1) openChapter(manifest[i + 1], false).catch(showError);
    };
    document.addEventListener('keydown', e => {
      if (e.altKey || e.metaKey || e.ctrlKey || ['INPUT','TEXTAREA','BUTTON','SELECT'].includes(document.activeElement?.tagName)) return;
      if (e.key === '1' || e.key === '2') take(Number(e.key) - 1, false);
    });
    const manifestDoc = await fetchJSON('interactive/manifest.json');
    manifest = manifestDoc.entries || [];
    const list = byId('chapter-list');
    if (!manifest.length) {
      byId('scene-body').textContent = 'The first interactive chapter has not been published. See GitHub Actions for the next run.';
      return;
    }
    for (const entry of manifest.slice(-36).reverse()) {
      const button = make('button', '#' + String(entry.chapter).padStart(6, '0') + ' / ' + entry.world_lens, 'chapter-select');
      button.type = 'button'; button.dataset.id = String(entry.chapter);
      button.onclick = () => openChapter(entry).catch(showError);
      list.append(button);
    }
    const old = readStore(storageKey);
    const entry = manifest.find(e => e.chapter === old?.chapter) || manifest[manifest.length - 1];
    await openChapter(entry, true);
    const m = await fetchJSON('book/manifest.json');
    byId('chapter-total').textContent = String((m.entries || []).length);
    try {
      const a = await fetchJSON('archive/manifest.json');
      const snapshots = a.snapshots || [];
      byId('archive-total').textContent = String(snapshots.length);
      const recent = snapshots[snapshots.length-1];
      if (recent) {
        byId('archive-date').textContent = 'Latest captured: ' + recent.captured_at;
      }
    } catch {/* Archive is a noncritical ancillary panel. */}
  }
  setup().catch(showError);
})();
