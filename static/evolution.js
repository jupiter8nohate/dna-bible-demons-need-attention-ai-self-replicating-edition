'use strict';
(async () => {
  const status = document.getElementById('evolution-status');
  const target = document.getElementById('evolution-latest');
  if (!status || !target) return;
  const write = (label, value) => {
    const p = document.createElement('p');
    const strong = document.createElement('strong');
    strong.textContent = label + ': ';
    p.append(strong, document.createTextNode(value));
    target.append(p);
  };
  const read = async path => {
    const response = await fetch(path, {cache:'no-store'});
    if (!response.ok) throw new Error('Evolution archive unavailable');
    return response.json();
  };
  try {
    const ledger = await read('evolution/manifest.json');
    if (ledger.schema_version !== 'dna.evolution.v1' || !Array.isArray(ledger.lessons) || !Array.isArray(ledger.trials)) throw Error('Schema mismatch');
    status.textContent = `${ledger.lessons.length} provisional lessons / ${ledger.trials.length} strategy trials`;
    if (ledger.lessons.length) {
      const last = ledger.lessons[ledger.lessons.length - 1];
      if (!/^lessons\/lesson-\d{6}\.json$/.test(last.path)) throw Error('Invalid lesson path');
      const lesson = await read('evolution/' + last.path);
      write('Latest lesson', `Chapter ${lesson.chapter_id} / ${lesson.status} / ${lesson.observations.join(', ')}`);
    }
    if (ledger.trials.length) {
      const last = ledger.trials[ledger.trials.length - 1];
      if (!/^trials\/trial-\d{6}\.json$/.test(last.path)) throw Error('Invalid trial path');
      const trial = await read('evolution/' + last.path);
      write('Strategy evaluation', `${trial.champion} vs. ${trial.best_candidate}: ${trial.decision.replace(/_/g, ' ')}`);
    }
  } catch (err) {
    status.textContent = 'Evolution records are not yet available or could not be loaded.';
  }
})();
