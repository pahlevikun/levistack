#!/usr/bin/env node
// What did I do in Jira? Ticket movement, creation, assignment changes and comments by the token's owner,
// inside a date window. Read-only. Node 20+, no npm deps. Use the Atlassian MCP instead if you have it.
//
//   JIRA_DOMAIN=acme.atlassian.net JIRA_EMAIL=me@acme.com JIRA_TOKEN=... \
//     node jira.mjs --start YYYY-MM-DD --end YYYY-MM-DD [--projects ABC,DEF] [--json]
//
// JIRA_DOMAIN and JIRA_EMAIL may also live in the config file (see collect.mjs) as jira.domain / jira.email,
// and projects as jira.projects. The token is only ever read from JIRA_TOKEN.
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const clip = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

/** Jira stamps look like 2026-10-03T14:02:11.123+0700; normalise the offset so every runtime parses them. */
export const jiraTs = (s) => Date.parse(String(s).replace(/([+-]\d\d)(\d\d)$/, '$1:$2')) / 1000;

/** Comments and descriptions arrive as Atlassian Document Format: a tree whose leaves are { text }. */
export function adfText(node) {
  if (!node) return '';
  if (typeof node === 'string') return node;
  if (node.type === 'text') return node.text ?? '';
  if (node.type === 'mention') return node.attrs?.text ?? '';
  const inner = (node.content ?? []).map(adfText).join(node.type === 'doc' ? '\n' : '');
  return inner;
}

/** The events one issue holds that were done by `me` inside the window. */
export function extractActivity(issue, { me, startTs, endTs }) {
  const inWindow = (s) => { const t = jiraTs(s); return t >= startTs && t <= endTs; };
  const events = [];
  const f = issue.fields ?? {};
  if (f.reporter?.accountId === me && f.created && inWindow(f.created)) events.push({ ts: jiraTs(f.created), kind: 'created', detail: `${f.issuetype?.name ?? 'issue'} created` });
  for (const h of issue.changelog?.histories ?? []) {
    if (h.author?.accountId !== me || !inWindow(h.created)) continue;
    for (const it of h.items ?? []) {
      const kind = it.field === 'status' ? 'moved' : it.field === 'assignee' ? 'assigned' : 'changed';
      events.push({ ts: jiraTs(h.created), kind, detail: `${it.field}: ${it.fromString || '∅'} → ${it.toString || '∅'}` });
    }
  }
  for (const c of f.comment?.comments ?? []) {
    if (c.author?.accountId !== me || !inWindow(c.created)) continue;
    events.push({ ts: jiraTs(c.created), kind: 'commented', detail: clip(adfText(c.body).replace(/\s+/g, ' ').trim(), 140) });
  }
  return events.sort((a, b) => a.ts - b.ts);
}

export function buildJql({ me, start, end, nextDay, projects }) {
  const q = `"${me}"`;
  const window = `("${start}", "${nextDay}")`;
  const mine = [`assignee = ${q}`, `reporter = ${q}`, `status CHANGED BY ${q} DURING ${window}`, `assignee WAS ${q} DURING ${window}`, `worklogAuthor = ${q}`];
  const scope = projects?.length ? ` AND project in (${projects.map((p) => `"${p}"`).join(', ')})` : '';
  return `(${mine.join(' OR ')}) AND updated >= "${start}"${scope} ORDER BY updated DESC`;
}

async function api(base, auth, path) {
  const res = await fetch(`${base}${path}`, { headers: { Authorization: auth, Accept: 'application/json' }, signal: AbortSignal.timeout(30000) });
  if (res.status === 401) throw new Error('401 from Jira: check JIRA_EMAIL and JIRA_TOKEN (create a token at id.atlassian.com/manage-profile/security/api-tokens)');
  if (res.status === 403) throw new Error('403 from Jira: the token owner cannot see that project or issue');
  if (!res.ok) throw new Error(`Jira answered ${res.status} for ${path.split('?')[0]}`);
  return res.json();
}

export async function collect({ domain, email, token, start, end, projects }) {
  const base = /^https?:\/\//.test(domain) ? domain.replace(/\/$/, '') : `https://${domain}`;
  const auth = `Basic ${Buffer.from(`${email}:${token}`).toString('base64')}`;
  const me = (await api(base, auth, '/rest/api/3/myself')).accountId;
  const nextDay = new Date(Date.parse(`${end}T00:00:00Z`) + 86400000).toISOString().slice(0, 10);
  const jql = buildJql({ me, start, end, nextDay, projects });
  const [y, m, d] = start.split('-').map(Number);
  const [y2, m2, d2] = end.split('-').map(Number);
  const startTs = new Date(y, m - 1, d, 0, 0, 0).getTime() / 1000;
  const endTs = new Date(y2, m2 - 1, d2, 23, 59, 59).getTime() / 1000;
  const issues = [];
  let token_ = '';
  for (let page = 0; page < 10; page++) {
    // /search/jql is the current endpoint; the older /search was retired on Jira Cloud.
    const qs = new URLSearchParams({ jql, fields: 'summary,status,issuetype,created,reporter,comment', expand: 'changelog', maxResults: '100' });
    if (token_) qs.set('nextPageToken', token_);
    const data = await api(base, auth, `/rest/api/3/search/jql?${qs}`);
    issues.push(...(data.issues ?? []));
    token_ = data.nextPageToken;
    if (!token_) break;
  }
  const out = [];
  for (const issue of issues) {
    const events = extractActivity(issue, { me, startTs, endTs });
    if (events.length) out.push({ key: issue.key, summary: issue.fields.summary, status: issue.fields.status?.name, type: issue.fields.issuetype?.name, url: `${base}/browse/${issue.key}`, events });
  }
  return { me, candidates: issues.length, issues: out };
}

function format(r, { start, end }) {
  const lines = [`## Jira (${start} – ${end}; ${r.issues.length} of ${r.candidates} candidate issues had activity by you)`];
  for (const i of r.issues) {
    lines.push(`### ${i.key} ${i.summary} [${i.status}]`);
    for (const e of i.events) lines.push(`- ${new Date(e.ts * 1000).toLocaleString('sv').slice(0, 16)}  ${e.kind}: ${e.detail}`);
  }
  return lines.join('\n');
}

function loadJiraConfig() {
  const file = process.env.STANDUP_CONFIG || join(homedir(), '.config/standup/config.json');
  try { return existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')).jira ?? {} : {}; } catch { return {}; }
}

async function main(argv) {
  const { values: v } = parseArgs({ args: argv, options: { start: { type: 'string' }, end: { type: 'string' }, projects: { type: 'string' }, json: { type: 'boolean' } } });
  const cfg = loadJiraConfig();
  const domain = process.env.JIRA_DOMAIN || cfg.domain;
  const email = process.env.JIRA_EMAIL || cfg.email;
  const token = process.env.JIRA_TOKEN;
  if (!v.start || !v.end) throw new Error('--start and --end (YYYY-MM-DD) are required');
  if (!domain || !email || !token) throw new Error('set JIRA_DOMAIN, JIRA_EMAIL and JIRA_TOKEN (the token only via the environment)');
  const projects = v.projects ? v.projects.split(',') : cfg.projects;
  const r = await collect({ domain, email, token, start: v.start, end: v.end, projects });
  console.log(v.json ? JSON.stringify(r, null, 2) : format(r, v));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch((e) => { console.error(`jira: ${e.message}`); process.exitCode = 1; });
}
