import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync, symlinkSync, mkdtempSync, writeFileSync, rmSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { spawnSync } from 'node:child_process';
import vm from 'node:vm';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseCsv, check } from '../skills/product/ui-ux-kit/scripts/check-acceptance.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const product = join(root, 'skills', 'product');
const craft = join(product, 'ui-ux-kit');
const color = join(product, 'color-kit');
const read = (p) => readFileSync(p, 'utf8');
const table = (p) => {
  const rows = parseCsv(read(p));
  const [header, ...body] = rows;
  return { header, body, objects: body.map((r) => Object.fromEntries(header.map((h, i) => [h, r[i]]))) };
};

test('every CSV in the product skills has rows as wide as its header', () => {
  const files = [];
  for (const skill of ['ui-ux-kit', 'color-kit']) {
    for (const dir of ['data', 'templates']) {
      const d = join(product, skill, dir);
      if (existsSync(d)) for (const f of readdirSync(d)) if (f.endsWith('.csv')) files.push(join(d, f));
    }
  }
  assert.ok(files.length >= 8, `found ${files.length} csv files`);
  for (const f of files) {
    const { header, body } = table(f);
    assert.ok(body.length > 0, `${f} has no rows`);
    body.forEach((r, i) => assert.equal(r.length, header.length, `${f} row ${i + 2} has ${r.length} columns, header has ${header.length}`));
  }
});

test('ux-rules.csv: unique ids, known platforms and severities, evidence kinds', () => {
  const { objects, header } = table(join(craft, 'data', 'ux-rules.csv'));
  assert.deepEqual(header, ['id', 'area', 'platform', 'rule', 'check', 'severity', 'evidence']);
  const platforms = new Set(['all', 'ios', 'android', 'mobile', 'tablet', 'react-native', 'flutter', 'web', 'desktop', 'tv', 'car']);
  const severities = new Set(['critical', 'high', 'medium', 'low']);
  const evidence = new Set(['render', 'device', 'source', 'test']);
  const ids = new Set();
  for (const r of objects) {
    assert.ok(/^[A-Z0-9]+-\d{2}$/.test(r.id), `bad id ${r.id}`);
    assert.ok(!ids.has(r.id), `duplicate id ${r.id}`);
    ids.add(r.id);
    assert.ok(platforms.has(r.platform), `${r.id}: unknown platform ${r.platform}`);
    assert.ok(severities.has(r.severity), `${r.id}: unknown severity ${r.severity}`);
    assert.ok(evidence.has(r.evidence), `${r.id}: unknown evidence ${r.evidence}`);
  }
  // car and tv are first-class: each has critical rules.
  for (const p of ['car', 'tv']) assert.ok(objects.some((r) => r.platform === p && r.severity === 'critical'), `${p} needs a critical rule`);
  assert.ok(objects.length >= 105);
});

test('every rule id mentioned anywhere in ui-ux-kit exists', () => {
  const ids = new Set(table(join(craft, 'data', 'ux-rules.csv')).objects.map((r) => r.id));
  const walk = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]));
  const files = walk(craft).filter((f) => /\.(md|csv)$/.test(f) && !f.endsWith('ux-rules.csv'));
  const idPattern = /\b((?:A11Y|TOUCH|NAV|FORM|FEED|MOTION|LAYOUT|TYPE|THEME|PERF|CONTENT|PERM|HAPTIC|CAR|TV|DESK|PAY)-\d{2})\b/g;
  let seen = 0;
  for (const f of files) for (const m of read(f).matchAll(idPattern)) { seen++; assert.ok(ids.has(m[1]), `${f} cites unknown rule ${m[1]}`); }
  assert.ok(seen >= 2, 'expected at least the template to cite rule ids');
});

test('the acceptance checker fails a bad file when run through a symlink or a path with a space', () => {
  const dir = mkdtempSync(join(tmpdir(), 'ux accept '));
  try {
    const script = join(craft, 'scripts', 'check-acceptance.mjs');
    const link = join(dir, 'check-link.mjs');
    symlinkSync(script, link);
    const bad = join(dir, 'bad file.csv');
    writeFileSync(bad, 'Feature ID,Surface\nUX001,a\n');
    for (const s of [script, link]) {
      const r = spawnSync('node', [s, bad], { encoding: 'utf8' });
      assert.equal(r.status, 1, `${s} should fail a bad csv, got ${r.status}: ${r.stdout}${r.stderr}`);
    }
    const good = spawnSync('node', [link, join(craft, 'templates', 'ux-acceptance.csv')], { encoding: 'utf8' });
    assert.equal(good.status, 0, good.stderr);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('the acceptance template passes the acceptance checker and bad files fail it', () => {
  assert.deepEqual(check(read(join(craft, 'templates', 'ux-acceptance.csv'))), []);
  const header = 'Feature ID,Surface,Feature / capability,User story,Expected behavior based on code,Code anchors,Initial test approach,Initial test command or route,Status,Test result,Errors,Fix status,Retest result,Notes';
  const bad = `${header}\nUX001,a,b,c,d,,e,f,Passed,,,,,\nUX001,a,b,c,d,x.ts,e,f,Weird,,,,,\n3bad,a,b,c,,x.ts,e,f,Not Tested,,,,,\nshort,row\n`;
  const errors = check(bad).join('\n');
  assert.match(errors, /at least one code anchor/);
  assert.match(errors, /duplicate Feature ID/);
  assert.match(errors, /unknown status/);
  assert.match(errors, /expected behavior is empty/);
  assert.match(errors, /columns, expected 14/);
  assert.match(errors, /should look like/);
  assert.match(errors, /needs a test result/);
});

test('motion-bands.csv covers car and tv and every duration row has an easing', () => {
  const { objects } = table(join(craft, 'data', 'motion-bands.csv'));
  assert.ok(objects.some((r) => r.platform === 'car'));
  assert.ok(objects.some((r) => r.platform === 'tv'));
  for (const r of objects) assert.ok(r.easing && r.duration, `${r.purpose} lacks duration or easing`);
});

test('stack-notes.csv covers the stacks the skill promises', () => {
  const stacks = new Set(table(join(craft, 'data', 'stack-notes.csv')).objects.map((r) => r.stack));
  for (const s of ['swiftui', 'compose', 'react-native', 'flutter', 'react', 'nextjs', 'vue', 'nuxt', 'svelte', 'tailwind']) assert.ok(stacks.has(s), `missing stack ${s}`);
});

test('every platform guide that SKILL.md names exists', () => {
  const skill = read(join(craft, 'SKILL.md'));
  const paths = [...skill.matchAll(/`(references\/[^`]+\.md)`/g)].map((m) => m[1]);
  assert.ok(paths.length >= 14);
  for (const p of paths) assert.ok(existsSync(join(craft, p)), `${p} is named in SKILL.md but missing`);
  for (const p of ['ios', 'android-compose', 'react-native', 'flutter', 'desktop', 'web', 'car', 'tv']) assert.ok(existsSync(join(craft, 'references', 'platforms', `${p}.md`)));
});

test('color-kit data: roles cover the kit tokens and pairs use known modes', () => {
  const roles = table(join(color, 'data', 'roles.csv')).objects.map((r) => r.role);
  for (const r of ['background', 'surface', 'text', 'text-muted', 'primary', 'on-primary', 'link', 'focus-ring', 'danger', 'success', 'warning', 'info']) assert.ok(roles.includes(r), `roles.csv lacks ${r}`);
  const pairs = table(join(color, 'data', 'essential-pairs.csv')).objects;
  const modes = new Set(pairs.map((p) => p.mode));
  assert.deepEqual([...modes].sort(), ['dark', 'light']);
  for (const p of pairs) assert.ok(Number(p.need) >= 3, `${p.name} need`);
  const knobs = table(join(color, 'data', 'mood-to-knobs.csv')).objects;
  assert.ok(knobs.every((k) => k.knobs.startsWith('--')));
});

test('color-kit and ui-ux-kit SKILL.md files name each other and the kit', () => {
  const c = read(join(color, 'SKILL.md'));
  const i = read(join(craft, 'SKILL.md'));
  for (const name of ['ui-ux-kit', 'design-system-kit']) assert.match(c, new RegExp('- `' + name + '`'));
  for (const name of ['color-kit', 'design-system-kit']) assert.match(i, new RegExp('- `' + name + '`'));
});

const proto = join(product, 'prototype-wireframe');

test('prototype-wireframe: every file SKILL.md links to exists, and every reference is linked', () => {
  const skill = read(join(proto, 'SKILL.md'));
  const linked = [...skill.matchAll(/\]\(((?:references|templates)\/[^)#]+)\)/g)].map((m) => m[1]);
  for (const f of linked) assert.ok(existsSync(join(proto, f)), `${f} is linked but missing`);
  for (const f of readdirSync(join(proto, 'references'))) assert.ok(skill.includes(`references/${f}`), `${f} is not linked from SKILL.md`);
  for (const f of readdirSync(join(proto, 'templates'))) assert.ok(skill.includes(`templates/${f}`), `${f} is not named in SKILL.md`);
});

test('prototype-wireframe: the playground rule is pure, speaks plain words and every walkthrough runs', () => {
  const html = read(join(proto, 'templates', 'playground.html'));
  const js = html.match(/<script>([\s\S]*)<\/script>/)[1];
  const els = {};
  const ctx = vm.createContext({ document: { getElementById: (id) => (els[id] ??= { textContent: '', innerHTML: '', className: '' }) } });
  vm.runInContext(js + '\nthis.t={RULE,send,go,start,get S(){return S},get log(){return log}};', ctx);
  const { RULE, start, go } = ctx.t;
  assert.doesNotMatch(js.slice(js.indexOf('const RULE'), js.indexOf('// ===== PAGE')), /document|window|getElementById/, 'rule block must not touch the page');
  for (const s of Object.keys(RULE.states)) assert.ok(RULE.words.state[s], `no plain word for state ${s}`);
  const events = new Set(Object.values(RULE.states).flatMap((x) => Object.keys(x)));
  for (const e of events) assert.ok(RULE.words.event[e], `no plain word for event ${e}`);
  for (const k of Object.keys(RULE.context)) assert.ok(RULE.words.field[k], `no plain word for field ${k}`);
  let refused = 0;
  for (const [name, w] of Object.entries(RULE.walks)) {
    start(name);
    w.steps.forEach((_, i) => { go(i); if (/Refused/.test(ctx.t.log[0])) refused++; });
  }
  assert.equal(refused, 1, 'exactly the one illegal walkthrough is refused');
});

test('prototype-wireframe: the receipt names the fields a reader needs', () => {
  const r = read(join(proto, 'templates', 'receipt.md'));
  for (const h of ['Question', 'Home', 'How to run', 'Score', 'Prototype now']) assert.match(r, new RegExp(h), `receipt lacks ${h}`);
});

test('color-facts.csv: unique ids, known topics, every row has a use and a check', () => {
  const { header, objects } = table(join(color, 'data', 'color-facts.csv'));
  assert.deepEqual(header, ['id', 'topic', 'fact', 'product_use', 'check']);
  assert.ok(objects.length >= 45, `only ${objects.length} facts`);
  const topics = new Set(['perception', 'spaces', 'lightness', 'warm-cool', 'mixing', 'print', 'meaning', 'data-viz', 'accessibility']);
  const seen = new Set();
  for (const r of objects) {
    assert.match(r.id, /^[A-Z]{3}-\d{2}$/, r.id);
    assert.ok(!seen.has(r.id), `duplicate ${r.id}`);
    seen.add(r.id);
    assert.ok(topics.has(r.topic), `${r.id} has unknown topic ${r.topic}`);
    for (const col of ['fact', 'product_use', 'check']) assert.ok(r[col] && r[col].length > 15, `${r.id} lacks ${col}`);
  }
  const doc = read(join(color, 'references', 'color-science-for-products.md'));
  for (const t of topics) assert.ok(doc.includes('`' + t + '`'), `topic ${t} is not explained in the guide`);
});

test('color-kit: every reference is linked from SKILL.md and every theme.py command it names exists', () => {
  const skill = read(join(color, 'SKILL.md'));
  for (const f of readdirSync(join(color, 'references'))) assert.ok(skill.includes(`references/${f}`), `${f} is not linked from SKILL.md`);
  const script = join(product, 'design-system-kit', 'specialities', 'design-system', 'scripts', 'theme', 'theme.py');
  const help = spawnSync('python3', ['-B', '-I', script, '--help'], { encoding: 'utf8' });
  assert.equal(help.status, 0, help.stderr);
  const real = new Set([...help.stdout.matchAll(/\b(list|explore|build|check|contrast|audit|bind|name|scale|mix)\b/g)].map((m) => m[1]));
  const docs = [join(color, 'SKILL.md'), ...readdirSync(join(color, 'references')).map((f) => join(color, 'references', f))];
  let named = 0;
  for (const f of docs) {
    for (const m of read(f).matchAll(/theme\.py (\w+)/g)) {
      named++;
      assert.ok(real.has(m[1]), `${f} names an unknown command theme.py ${m[1]}`);
    }
  }
  assert.ok(named >= 10, 'expected the docs to name the commands');
});

test('color-kit: the brief template only holds keys the builder knows', () => {
  const brief = JSON.parse(read(join(color, 'templates', 'color-brief.json')));
  const known = new Set(['brief', 'seed', 'domain', 'mood', 'hue', 'accent_hue', 'chroma', 'temp', 'ground', 'harmony', 'shape', 'voice', 'motion',
    'signature', 'neutral', 'density', 'danger_hue', 'region', 'platform', 'color_amount', 'neutral_temp']);
  for (const k of Object.keys(brief)) assert.ok(known.has(k), `unknown brief key ${k}`);
});
