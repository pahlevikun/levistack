#!/usr/bin/env node
// Validate a ux-acceptance.csv: columns, row widths, unique IDs, known statuses, and at least one code anchor per row.
// Usage: node check-acceptance.mjs ux-acceptance.csv
import { readFileSync, realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const COLUMNS = [
  'Feature ID', 'Surface', 'Feature / capability', 'User story', 'Expected behavior based on code', 'Code anchors',
  'Initial test approach', 'Initial test command or route', 'Status', 'Test result', 'Errors', 'Fix status', 'Retest result', 'Notes',
];
const STATUSES = new Set([
  'Not Tested', 'Passed', 'Failed - Product', 'Failed - UX', 'Failed - Logistical', 'Failed - Test Infra', 'Blocked - Env', 'Fixed', 'Passed after fix',
]);

export function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') { quoted = false; } else { cell += c; }
    } else if (c === '"') {
      quoted = true;
    } else if (c === ',') {
      row.push(cell); cell = '';
    } else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cell); cell = '';
      if (row.some((v) => v !== '')) rows.push(row);
      row = [];
    } else {
      cell += c;
    }
  }
  if (cell !== '' || row.length) { row.push(cell); if (row.some((v) => v !== '')) rows.push(row); }
  return rows;
}

export function check(text) {
  const errors = [];
  const rows = parseCsv(text);
  if (!rows.length) return ['file is empty'];
  const header = rows[0];
  if (header.join('|') !== COLUMNS.join('|')) errors.push(`header must be exactly: ${COLUMNS.join(',')}`);
  const seen = new Set();
  rows.slice(1).forEach((r, i) => {
    const line = i + 2;
    if (r.length !== COLUMNS.length) { errors.push(`row ${line}: ${r.length} columns, expected ${COLUMNS.length}`); return; }
    const [id, , , , expected, anchors, , , status] = r;
    if (!/^[A-Za-z][A-Za-z0-9]*[-_]?\d{1,5}$/.test(id)) errors.push(`row ${line}: Feature ID "${id}" should look like UX001 or AUTH-01`);
    if (seen.has(id)) errors.push(`row ${line}: duplicate Feature ID ${id}`);
    seen.add(id);
    if (!expected.trim()) errors.push(`row ${line}: expected behavior is empty`);
    if (!anchors.trim()) errors.push(`row ${line}: a row needs at least one code anchor`);
    if (!STATUSES.has(status)) errors.push(`row ${line}: unknown status "${status}"`);
    if ((status === 'Passed' || status === 'Passed after fix') && !r[9].trim()) errors.push(`row ${line}: a passed row needs a test result from this session`);
  });
  return errors;
}

const isMain = process.argv[1] && realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url));
if (isMain) {
  const file = process.argv[2];
  if (!file) { console.error('usage: node check-acceptance.mjs ux-acceptance.csv'); process.exit(2); }
  const errors = check(readFileSync(file, 'utf8'));
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  console.log('ok: ux-acceptance.csv is valid');
}
