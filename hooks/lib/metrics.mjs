import { appendFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { levistackHome } from './files.mjs';

// Best-effort JSONL log of gate decisions: $LEVISTACK_METRICS_DIR or ~/.levistack/metrics/gate-events.jsonl.
export function logEvent(hook, fields = {}) {
  try {
    const dir = process.env.LEVISTACK_METRICS_DIR || join(levistackHome(), 'metrics');
    mkdirSync(dir, { recursive: true });
    const ts = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
    appendFileSync(join(dir, 'gate-events.jsonl'), `${JSON.stringify({ ts, hook, ...fields })}\n`);
  } catch {
    // metrics are optional
  }
}
