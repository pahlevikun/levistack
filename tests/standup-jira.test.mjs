import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { test } from 'node:test';
import { adfText, buildJql, collect, extractActivity, jiraTs } from '../skills/workflow/standup/scripts/jira.mjs';

const ME = 'acct-me';
const OTHER = 'acct-other';
const startTs = Date.parse('2026-10-06T00:00:00+07:00') / 1000;
const endTs = Date.parse('2026-10-06T23:59:59+07:00') / 1000;

const adf = (text) => ({ type: 'doc', content: [{ type: 'paragraph', content: [{ type: 'text', text }] }] });

const issue = {
  key: 'ABC-12',
  fields: {
    summary: 'Retry flaky upload',
    status: { name: 'In Review' },
    issuetype: { name: 'Bug' },
    created: '2026-10-06T09:00:00.000+0700',
    reporter: { accountId: ME },
    comment: {
      comments: [
        { author: { accountId: ME }, created: '2026-10-06T15:00:00.000+0700', body: adf('Pushed a fix, MR is up') },
        { author: { accountId: OTHER }, created: '2026-10-06T16:00:00.000+0700', body: adf('looks good') },
        { author: { accountId: ME }, created: '2026-10-09T10:00:00.000+0700', body: adf('outside window') },
      ],
    },
  },
  changelog: {
    histories: [
      { author: { accountId: ME }, created: '2026-10-06T10:30:00.000+0700', items: [{ field: 'status', fromString: 'To Do', toString: 'In Progress' }] },
      { author: { accountId: OTHER }, created: '2026-10-06T11:00:00.000+0700', items: [{ field: 'status', fromString: 'In Progress', toString: 'Blocked' }] },
      { author: { accountId: ME }, created: '2026-10-06T14:00:00.000+0700', items: [{ field: 'assignee', fromString: null, toString: 'Me' }, { field: 'Sprint', fromString: '', toString: 'Sprint 5' }] },
      { author: { accountId: ME }, created: '2026-10-02T10:00:00.000+0700', items: [{ field: 'status', fromString: 'Open', toString: 'To Do' }] },
    ],
  },
};

test('jiraTs: parses Jira offsets without a colon', () => {
  assert.equal(jiraTs('2026-10-06T00:00:00.000+0700'), Date.parse('2026-10-06T00:00:00+07:00') / 1000);
});

test('adfText: flattens a document tree, including mentions', () => {
  assert.equal(adfText(adf('hello')), 'hello');
  assert.equal(adfText({ type: 'doc', content: [{ type: 'paragraph', content: [{ type: 'mention', attrs: { text: '@sam' } }, { type: 'text', text: ' please look' }] }] }), '@sam please look');
  assert.equal(adfText(null), '');
});

test('extractActivity: keeps only what I did inside the window, in time order', () => {
  const ev = extractActivity(issue, { me: ME, startTs, endTs });
  assert.deepEqual(ev.map((e) => `${e.kind}|${e.detail}`), [
    'created|Bug created',
    'moved|status: To Do → In Progress',
    'assigned|assignee: ∅ → Me',
    'changed|Sprint: ∅ → Sprint 5',
    'commented|Pushed a fix, MR is up',
  ]);
});

test('extractActivity: an issue someone else touched yields nothing for me', () => {
  assert.deepEqual(extractActivity(issue, { me: 'nobody', startTs, endTs }), []);
});

test('buildJql: covers assignee, reporter, movement and worklogs, and scopes to projects', () => {
  const jql = buildJql({ me: ME, start: '2026-10-06', end: '2026-10-06', nextDay: '2026-10-07', projects: ['ABC', 'DEF'] });
  assert.match(jql, /status CHANGED BY "acct-me" DURING \("2026-10-06", "2026-10-07"\)/);
  assert.match(jql, /worklogAuthor = "acct-me"/);
  assert.match(jql, /project in \("ABC", "DEF"\)/);
  assert.ok(!buildJql({ me: ME, start: 'a', end: 'b', nextDay: 'c' }).includes('project in'));
});

function mockJira(handler) {
  return new Promise((resolve) => {
    const seen = [];
    const server = createServer((req, res) => {
      seen.push({ url: req.url, auth: req.headers.authorization });
      handler(req, res);
    });
    server.listen(0, '127.0.0.1', () => resolve({ server, seen, base: `http://127.0.0.1:${server.address().port}` }));
  });
}
const json = (res, body, status = 200) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(body)); };

test('collect: resolves the account, pages through results, and returns only issues with my activity', async () => {
  const quiet = { key: 'ABC-99', fields: { summary: 'Untouched by me', status: { name: 'To Do' }, issuetype: { name: 'Task' }, reporter: { accountId: OTHER }, created: '2026-09-01T09:00:00.000+0700' } };
  const { server, seen, base } = await mockJira((req, res) => {
    if (req.url.startsWith('/rest/api/3/myself')) return json(res, { accountId: ME });
    if (req.url.includes('nextPageToken=p2')) return json(res, { issues: [quiet] });
    return json(res, { issues: [issue], nextPageToken: 'p2' });
  });
  try {
    const r = await collect({ domain: base, email: 'me@example.com', token: 'tkn', start: '2026-10-06', end: '2026-10-06' });
    assert.equal(r.candidates, 2);
    assert.deepEqual(r.issues.map((i) => i.key), ['ABC-12']);
    assert.equal(r.issues[0].url, `${base}/browse/ABC-12`);
    assert.equal(seen[0].auth, `Basic ${Buffer.from('me@example.com:tkn').toString('base64')}`);
    assert.ok(seen.some((s) => s.url.startsWith('/rest/api/3/search/jql?')));
    assert.ok(seen.every((s) => !s.url.startsWith('/rest/api/3/search?')));
  } finally {
    server.close();
  }
});

test('collect: turns 401 and 403 into messages that say what to fix', async () => {
  for (const [status, re] of [[401, /JIRA_EMAIL and JIRA_TOKEN/], [403, /cannot see/]]) {
    const { server, base } = await mockJira((req, res) => json(res, {}, status));
    try {
      await assert.rejects(collect({ domain: base, email: 'e', token: 't', start: '2026-10-06', end: '2026-10-06' }), re);
    } finally {
      server.close();
    }
  }
});
