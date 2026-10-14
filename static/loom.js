'use strict';
(() => {
  const status = document.getElementById('loom-status');
  const missions = document.getElementById('loom-missions');
  if (!status || !missions) return;
  const put = (parent, tag, value, className) => {
    const el = document.createElement(tag);
    el.textContent = value;
    if (className) el.className = className;
    parent.append(el);
    return el;
  };
  async function getJson(url) {
    const response = await fetch(url, {cache: 'no-store'});
    if (!response.ok) throw Error('Plan not published');
    return response.json();
  }
  (async () => {
    try {
      const ledger = await getJson('covenant/manifest.json');
      if (ledger.schema_version !== 'dna.witness-loom.v1' || !Array.isArray(ledger.entries) || !ledger.entries.length) {
        status.textContent = 'No Witness Loom missions have been published yet.';
        return;
      }
      const last = ledger.entries[ledger.entries.length - 1];
      if (!/^plans\/plan-\d{6}\.json$/.test(last.path)) throw Error('Invalid plan path');
      const plan = await getJson('covenant/' + last.path);
      if (plan.schema_version !== 'dna.witness-loom.v1' || plan.registered_cells !== 666 || plan.human_canon_write_allowed !== false) {
        throw Error('Invalid plan policy');
      }
      status.textContent = `${plan.slot} UTC | ${plan.active_hexads} leased hexads | ${plan.resting_hexads} resting | 666 registered identities`;
      missions.replaceChildren();
      const focus = plan.focus || {};
      put(missions, 'p', `Primary question: ${String(focus.question || 'Not available').slice(0, 250)}`);
      put(missions, 'p', `Evidence: ${focus.evidence_status || 'unknown'} | No authority over the human canon`, 'bar');
      for (const mission of (plan.missions || []).slice(0, 6)) {
        put(missions, 'p', `${mission.hexad}: ${mission.focus_id} | 6 cells | 1-cycle lease`);
      }
    } catch (err) {
      status.textContent = 'Witness Loom publication unavailable or invalid. See the GitHub repository ledger.';
    }
  })();
})();
