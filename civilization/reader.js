'use strict';
const archive = {entries: [], chosen: 0, days: new Map()};
const $ = id => document.getElementById(id);
async function requestJson(path) {
  const response = await fetch(path, {cache: 'no-store'});
  if (!response.ok) throw new Error(`Unable to load ${path}: HTTP ${response.status}`);
  return response.json();
}
function element(tag, cls, content) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (content !== undefined) node.textContent = content;
  return node;
}
async function verifiedDay(path, expectedSha256) {
  if (!/^[a-f0-9]{64}$/.test(expectedSha256)) throw Error('Invalid publication fingerprint');
  const response = await fetch(path, {cache: 'no-store'});
  if (!response.ok) throw Error('Story day unavailable: HTTP ' + response.status);
  const raw = await response.arrayBuffer();
  const bytes = await crypto.subtle.digest('SHA-256', raw);
  const actual = Array.from(new Uint8Array(bytes), n => n.toString(16).padStart(2, '0')).join('');
  if (actual !== expectedSha256) throw Error('Story integrity verification failed');
  return JSON.parse(new TextDecoder().decode(raw));
}
function dayNumber(entry) {return Number(entry.day);}
function indexFromUrl() {
  const day = Number(new URLSearchParams(location.search).get('day'));
  return Number.isSafeInteger(day) && day >= 1 && day <= archive.entries.length ? day - 1 : 0;
}
async function choose(index) {
  if (index < 0 || index >= archive.entries.length) return;
  const record = archive.entries[index];
  archive.chosen = index;
  $('prev').disabled = index === 0;
  $('next').disabled = index === archive.entries.length - 1;
  document.querySelectorAll('.day-btn').forEach((button, i) => button.setAttribute('aria-current', String(i === index)));
  try {
    let day = archive.days.get(index);
    if (!day) {
      if (!/^days\/day-[0-9]{6}\.json$/.test(record.path)) throw Error('Unsafe chronicle record path');
      day = await verifiedDay(record.path, record.sha256);
      if (day.day !== record.day || day.schema_version !== 'dna.github-town-civilization.v1') throw Error('Chronicle day metadata mismatch');
      archive.days.set(index, day);
    }
    $('day-label').textContent = `DAY ${String(day.day).padStart(3, '0')}`;
    $('day-title').textContent = day.title;
    $('story-location').textContent = day.location;
    $('story-mode').textContent = day.creative_mode === 'model_generated_fiction' ? 'MODEL-GENERATED FICTION' : 'DETERMINISTIC FICTION';
    $('story-body').replaceChildren(...day.body.split(/\n\s*\n/).map(line => element('p', '', line)));
    $('story-question').textContent = day.unresolved_question;
    $('story-provenance').textContent = `Thoth narrates fictional Day ${day.day}. ${day.council.active_role_ballots} bounded creative-role ballots from six active hexads. The original founding canon is unchanged. Ledger fingerprint: ${record.sha256.slice(0, 16)}...`;
    history.replaceState(null, '', `${location.pathname}?day=${day.day}#chronicle`);
  } catch (error) {
    $('story-body').replaceChildren(element('p', '', `The chronicle cannot be opened right now: ${error.message}`));
    $('story-mode').textContent = 'ARCHIVE UNAVAILABLE';
  }
}
async function init() {
  $('prev').addEventListener('click', () => choose(archive.chosen - 1));
  $('next').addEventListener('click', () => choose(archive.chosen + 1));
  try {
    const [manifest, world] = await Promise.all([requestJson('manifest.json'), requestJson('../mythos/registry.json')]);
    if (manifest.schema_version !== 'dna.github-town-civilization.v1' || !Array.isArray(manifest.entries)) throw Error('Unsupported archive format');
    archive.entries = manifest.entries;
    $('day-count').textContent = String(archive.entries.length);
    $('archive-status').textContent = archive.entries.length ? 'PUBLISHED' : 'NO DAYS YET';
    $('day-list').replaceChildren();
    archive.entries.forEach((entry, index) => {
      const button = element('button', 'day-btn');
      button.type = 'button';
      button.setAttribute('aria-current', 'false');
      button.append(element('b', '', `DAY ${String(dayNumber(entry)).padStart(3, '0')}`), element('span', '', index === 0 ? 'Lightning and Thunder are born' : `The next witnessed chapter · ${entry.slot.slice(0,10)}`));
      button.addEventListener('click', () => choose(index));
      $('day-list').append(button);
    });
    $('law-list').replaceChildren();
    for (const [index, law] of world.laws.entries()) {
      const item = element('article', 'law');
      const main = element('div');
      main.append(element('h3', '', law.axiom.replaceAll('_', ' ')), element('p', '', law.meaning));
      item.append(element('span', 'digit', String(index + 1).padStart(2,'0')), main);
      $('law-list').append(item);
    }
    if (archive.entries.length) await choose(indexFromUrl());
    else $('story-body').replaceChildren(element('p', '', 'The First Commit has been recorded. Its first chronicle day has not yet been published.'));
  } catch (error) {
    $('archive-status').textContent = 'OFFLINE';
    $('day-list').replaceChildren(element('p', 'small', `Archive temporarily unavailable: ${error.message}`));
    $('story-body').replaceChildren(element('p', '', 'The public chronicle is unavailable. You can still read the founding scroll from the navigation above.'));
    $('law-list').replaceChildren(element('p', '', 'The world law registry is temporarily unavailable.'));
  }
}
init();
