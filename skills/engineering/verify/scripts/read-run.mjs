#!/usr/bin/env node
// Read a test run the way the gate requires: exit code AND executed counts. A run that executed nothing is not proof.
//
//   node read-run.mjs -- <command...>              run the command, show its output, then the verdict
//   node read-run.mjs --exit <code> [--file log]   read saved output (stdin when --file is omitted)
//   options: --json (machine-readable verdict), --runner <name> (skip detection)
//
// Runners recognized from their summary line: pytest, jest, vitest, node:test, ExUnit (mix test), go test,
// cargo test, rspec, phpunit. Anything else is "inconclusive" when the exit code is 0: read the output yourself.
// Exit status: 0 pass, 1 fail, 3 inconclusive, 2 usage error.
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const ANSI = /\u001b\[[0-9;]*[A-Za-z]/g;
const num = (m, i) => (m && m[i] !== undefined ? Number(m[i]) : 0);
const count = (text, re) => (text.match(re) ?? []).length;
const sumAll = (text, re, i) => [...text.matchAll(re)].reduce((n, m) => n + Number(m[i] ?? 0), 0);

// Each parser returns { runner, passed, failed, skipped } or null when its summary line is absent.
const PARSERS = [
  function pytest(t) {
    const lines = t.split('\n').filter((l) => /\b(passed|failed|errors?|skipped|deselected)\b.* in [\d.]+s|no tests ran/.test(l));
    const line = lines.at(-1);
    if (!line) return null;
    const n = (word) => num(line.match(new RegExp(`(\\d+) ${word}`)), 1);
    return { runner: 'pytest', passed: n('passed'), failed: n('failed') + n('errors?'), skipped: n('skipped') };
  },
  function vitest(t) {
    const m = t.match(/^\s*Tests\s+(.*)\(\d+\)\s*$/m);
    if (!m) return null;
    const n = (word) => num(m[1].match(new RegExp(`(\\d+) ${word}`)), 1);
    return { runner: 'vitest', passed: n('passed'), failed: n('failed'), skipped: n('skipped') + n('todo') };
  },
  function jest(t) {
    const m = t.match(/^Tests:\s+(.*)$/m);
    if (!m) return null;
    const n = (word) => num(m[1].match(new RegExp(`(\\d+) ${word}`)), 1);
    return { runner: 'jest', passed: n('passed'), failed: n('failed'), skipped: n('skipped') + n('todo') };
  },
  function exunit(t) {
    const m = t.match(/(\d+) tests?, (\d+) failures?(?:, (\d+) (?:excluded|skipped))?(?:, (\d+) (?:excluded|skipped))?/);
    if (!m) return null;
    const total = Number(m[1]);
    const failed = Number(m[2]);
    const skipped = num(m, 3) + num(m, 4);
    return { runner: 'ExUnit', passed: Math.max(total - failed - skipped, 0), failed, skipped };
  },
  function cargo(t) {
    if (!/test result: (ok|FAILED)\./.test(t) && !/running \d+ tests?/.test(t)) return null;
    const re = /test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored/g;
    return { runner: 'cargo test', passed: sumAll(t, re, 1), failed: sumAll(t, re, 2), skipped: sumAll(t, re, 3) };
  },
  function rspec(t) {
    const m = t.match(/(\d+) examples?, (\d+) failures?(?:, (\d+) pending)?/);
    if (!m) return null;
    const total = Number(m[1]);
    const failed = Number(m[2]);
    const skipped = num(m, 3);
    return { runner: 'rspec', passed: Math.max(total - failed - skipped, 0), failed, skipped };
  },
  function phpunit(t) {
    if (/No tests executed!/.test(t)) return { runner: 'phpunit', passed: 0, failed: 0, skipped: 0 };
    const ok = t.match(/OK \((\d+) tests?, \d+ assertions?\)/);
    if (ok) return { runner: 'phpunit', passed: Number(ok[1]), failed: 0, skipped: 0 };
    const m = t.match(/Tests: (\d+), Assertions: \d+(?:, Failures: (\d+))?(?:, Errors: (\d+))?(?:, Skipped: (\d+))?/);
    if (!m) return null;
    const failed = num(m, 2) + num(m, 3);
    const skipped = num(m, 4);
    return { runner: 'phpunit', passed: Math.max(Number(m[1]) - failed - skipped, 0), failed, skipped };
  },
  function nodetest(t) {
    const get = (word) => t.match(new RegExp(`^[ℹ#] ${word} (\\d+)\\s*$`, 'm'));
    const total = get('tests');
    if (!total) return null;
    const failed = num(get('fail'), 1) + num(get('cancelled'), 1);
    const skipped = num(get('skipped'), 1) + num(get('todo'), 1);
    return { runner: 'node:test', passed: num(get('pass'), 1), failed, skipped };
  },
  function gotest(t) {
    const verbose = { passed: count(t, /^\s*--- PASS/gm), failed: count(t, /^\s*--- FAIL/gm), skipped: count(t, /^\s*--- SKIP/gm) };
    if (verbose.passed + verbose.failed + verbose.skipped > 0) return { runner: 'go test', ...verbose };
    const pkgOk = count(t, /^ok\s+\S+/gm);
    const pkgFail = count(t, /^FAIL\s+\S+/gm);
    const noTests = count(t, /\[no test files\]|no tests to run/g);
    if (pkgOk + pkgFail + noTests === 0) return null;
    // Without -v, go reports per package. Count a passing package as one executed unit.
    return { runner: 'go test (per package; use -v for test counts)', passed: pkgOk, failed: pkgFail, skipped: 0 };
  },
];

export function parseSummary(text, runner) {
  const clean = text.replace(ANSI, '');
  const list = runner ? PARSERS.filter((p) => p.name.toLowerCase() === runner.toLowerCase().replace(/\s+/g, '')) : PARSERS;
  for (const parse of list) {
    const r = parse(clean);
    if (r) return r;
  }
  return null;
}

export function verdict({ exit, summary }) {
  const exitKnown = Number.isInteger(exit);
  if (!summary) {
    if (exitKnown && exit !== 0) return { verdict: 'fail', reason: `exit ${exit}` };
    return {
      verdict: 'inconclusive',
      reason: exitKnown
        ? 'exit 0 but no recognizable test summary; read the output and the executed count yourself'
        : 'no recognizable test summary and no exit code supplied',
    };
  }
  const executed = summary.passed + summary.failed + summary.skipped;
  if (summary.failed > 0) return { verdict: 'fail', reason: `${summary.failed} failed` };
  if (exitKnown && exit !== 0) return { verdict: 'fail', reason: `exit ${exit} although the summary shows no failures; read the full output` };
  if (executed === 0) return { verdict: 'inconclusive', reason: '0 tests executed: a run that ran nothing is not proof' };
  if (summary.passed === 0) return { verdict: 'inconclusive', reason: `all ${executed} tests were skipped; nothing passed` };
  if (!exitKnown) return { verdict: 'inconclusive', reason: 'summary looks clean but no exit code was supplied' };
  return { verdict: 'pass', reason: summary.skipped ? `${summary.skipped} skipped; confirm that is expected` : '' };
}

function parseArgs(argv) {
  const cut = argv.indexOf('--');
  const head = cut === -1 ? argv : argv.slice(0, cut);
  const command = cut === -1 ? [] : argv.slice(cut + 1);
  const opts = {};
  for (let i = 0; i < head.length; i++) {
    const a = head[i];
    if (a === '--json') opts.json = true;
    else if (['--exit', '--file', '--runner'].includes(a)) {
      if (head[i + 1] === undefined) throw new Error(`${a} needs a value`);
      opts[a.slice(2)] = head[++i];
    } else throw new Error(`unexpected argument "${a}"`);
  }
  return { opts, command };
}

function main() {
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`read-run: ${e.message}`);
    process.exit(2);
  }
  const { opts, command } = parsed;
  let text;
  let exit;
  if (command.length) {
    const r = spawnSync(command[0], command.slice(1), { encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
    if (r.error) {
      console.error(`read-run: could not run "${command[0]}": ${r.error.message}`);
      process.exit(2);
    }
    text = `${r.stdout ?? ''}${r.stderr ?? ''}`;
    process.stdout.write(text.endsWith('\n') || !text ? text : `${text}\n`);
    exit = r.status ?? 128;
  } else {
    try {
      text = readFileSync(opts.file ?? 0, 'utf8');
    } catch (e) {
      console.error(`read-run: ${e.message}`);
      process.exit(2);
    }
    if (opts.exit !== undefined) {
      exit = Number(opts.exit);
      if (!Number.isInteger(exit)) {
        console.error('read-run: --exit must be an integer');
        process.exit(2);
      }
    }
  }
  const summary = parseSummary(text, opts.runner);
  const v = verdict({ exit, summary });
  if (opts.json) console.log(JSON.stringify({ exit: exit ?? null, summary, ...v }));
  else {
    console.log('---');
    console.log(`runner:   ${summary?.runner ?? 'not recognized'}`);
    console.log(`exit:     ${exit ?? 'not supplied'}`);
    if (summary) console.log(`executed: ${summary.passed + summary.failed + summary.skipped} (passed ${summary.passed}, failed ${summary.failed}, skipped ${summary.skipped})`);
    console.log(`verdict:  ${v.verdict}${v.reason ? ` - ${v.reason}` : ''}`);
  }
  process.exit({ pass: 0, fail: 1, inconclusive: 3 }[v.verdict]);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
