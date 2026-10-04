#!/usr/bin/env node
// Detect a codebase's architecture style and list dependency-direction candidates.
//
//   node arch-scan.mjs detect <dir> [--json]   stack, style signals with evidence, a ranked guess
//   node arch-scan.mjs check  <dir> [--json] [--all]   boundary-violation candidates with file:line
//
// The output is a list of places to look, not findings. Confirm each by reading the code. Folder names are weak
// evidence; the check command reads imports to see which way dependencies actually point.
// Languages: TypeScript/JavaScript, Java, Kotlin, Go, PHP, C#, Python, Dart.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, extname, join, posix, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SKIP_DIRS = new Set(['node_modules', '.git', 'vendor', 'dist', 'build', 'target', '.gradle', '.idea', '__pycache__', '.venv', 'venv', 'obj', 'coverage', '.next', '.dart_tool', '.cache', 'out', 'generated']);
export const MAX_FILES = 20000;
const MAX_BYTES = 512 * 1024;
const LANG = { '.ts': 'ts', '.tsx': 'ts', '.js': 'ts', '.jsx': 'ts', '.mjs': 'ts', '.cjs': 'ts', '.java': 'java', '.kt': 'java', '.kts': 'java', '.go': 'go', '.php': 'php', '.cs': 'cs', '.py': 'py', '.dart': 'dart' };

// ---------------------------------------------------------------- layers
const LAYER_WORDS = {
  domain: ['domain', 'entities', 'entity', 'enterprise'],
  application: ['application', 'usecases', 'use-cases', 'use_cases', 'usecase', 'interactors'],
  infrastructure: ['infrastructure', 'infra', 'adapters', 'adapter', 'persistence', 'outbound', 'gateways'],
  presentation: ['presentation', 'interface', 'interfaces', 'web', 'api', 'controllers', 'controller', 'http', 'rest', 'grpc', 'cli', 'inbound', 'routes', 'endpoints', 'ui', 'views'],
};
const WORD_TO_LAYER = new Map(Object.entries(LAYER_WORDS).flatMap(([layer, words]) => words.map((w) => [w, layer])));
const COMPOSITION = new Set(['config', 'configuration', 'composition', 'bootstrap', 'main', 'cmd', 'wiring', 'di', 'container', 'startup', 'program']);
const TEST_SEG = new Set(['test', 'tests', '__tests__', 'spec', 'specs', 'e2e', 'fixtures', 'mocks', 'testing']);
const COLA_SUFFIX = [['-domain', 'domain'], ['-app', 'application'], ['-infrastructure', 'infrastructure'], ['-infra', 'infrastructure'], ['-adapter', 'presentation']];

export function classifySegments(segments, lang) {
  let layer = null;
  let prev = '';
  for (const raw of segments) {
    const s = raw.toLowerCase();
    if (s === 'ports' || s === 'port') {
      // A port interface is owned by the layer that needs it; words after it (inbound, outbound, in, out) describe direction only.
      return layer === 'domain' ? 'domain' : 'application';
    }
    if (COMPOSITION.has(s) && !(s === 'main' && prev === 'src')) return 'composition';
    const cola = COLA_SUFFIX.find(([suffix]) => s.endsWith(suffix));
    if (cola) layer = cola[1];
    else if (WORD_TO_LAYER.has(s)) layer = WORD_TO_LAYER.get(s); // the deepest matching segment wins
    else if (lang === 'java' && s === 'app') layer = 'application';
    prev = s;
  }
  return layer;
}

export const isTestPath = (segments) => segments.some((s) => TEST_SEG.has(s.toLowerCase()) || /(\.|_)(test|spec)$/.test(s.toLowerCase()));

// ---------------------------------------------------------------- imports
const lineOf = (text, index) => text.slice(0, index).split('\n').length;

export function extractImports(text, lang) {
  const out = [];
  const push = (spec, index) => spec && out.push({ spec, line: lineOf(text, index) });
  if (lang === 'ts') {
    for (const m of text.matchAll(/(?:import|export)\s[^'";]*?from\s*['"]([^'"]+)['"]|import\s*['"]([^'"]+)['"]|require\(\s*['"]([^'"]+)['"]\s*\)|import\(\s*['"]([^'"]+)['"]\s*\)/g)) push(m[1] ?? m[2] ?? m[3] ?? m[4], m.index);
  } else if (lang === 'java') {
    for (const m of text.matchAll(/^\s*import\s+(?:static\s+)?([\w.*]+)/gm)) push(m[1], m.index);
  } else if (lang === 'go') {
    for (const m of text.matchAll(/import\s+(?:\w+\s+)?"([^"]+)"/g)) push(m[1], m.index);
    for (const block of text.matchAll(/import\s*\(([\s\S]*?)\)/g)) for (const m of block[1].matchAll(/"([^"]+)"/g)) push(m[1], block.index + block[0].indexOf(m[0]));
  } else if (lang === 'php') {
    for (const m of text.matchAll(/^\s*use\s+(?:function\s+|const\s+)?([\w\\]+)/gm)) push(m[1], m.index);
  } else if (lang === 'cs') {
    for (const m of text.matchAll(/^\s*using\s+(?:static\s+)?([\w.]+)\s*;/gm)) push(m[1], m.index);
  } else if (lang === 'py') {
    for (const m of text.matchAll(/^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))/gm)) push(m[1] ?? m[2], m.index);
  } else if (lang === 'dart') {
    for (const m of text.matchAll(/^\s*(?:import|export)\s+['"]([^'"]+)['"]/gm)) push(m[1], m.index);
  }
  return out;
}

const ownNamespace = (text, lang) => {
  if (lang === 'java') return text.match(/^\s*package\s+([\w.]+)/m)?.[1] ?? '';
  if (lang === 'php') return text.match(/^\s*namespace\s+([\w\\]+)/m)?.[1] ?? '';
  if (lang === 'cs') return text.match(/^\s*namespace\s+([\w.]+)/m)?.[1] ?? '';
  return '';
};

// ---------------------------------------------------------------- technology deny lists
// kind 'framework' is flagged in the domain only; kind 'tech' (databases, HTTP and broker clients) in domain and application.
const D = (kind, ...prefixes) => prefixes.map((p) => ({ p, kind }));
export const DENY = {
  ts: [...D('framework', 'express', 'fastify', '@nestjs/', 'koa', 'hono', 'next', 'react', 'class-validator', 'class-transformer'), ...D('tech', 'typeorm', 'prisma', '@prisma/', 'mongoose', 'sequelize', 'knex', 'drizzle-orm', 'axios', 'node-fetch', 'pg', 'mysql', 'mysql2', 'redis', 'ioredis', 'kafkajs', 'amqplib')],
  java: [...D('framework', 'org.springframework.', 'jakarta.servlet', 'javax.servlet', 'jakarta.ws.rs', 'javax.ws.rs', 'com.fasterxml.jackson.', 'io.micronaut.', 'io.quarkus.'), ...D('tech', 'jakarta.persistence', 'javax.persistence', 'org.hibernate.', 'org.jooq.', 'org.mybatis.', 'org.apache.kafka.', 'org.springframework.data.', 'org.springframework.jdbc.')],
  go: [...D('framework', 'github.com/gin-gonic/', 'github.com/labstack/echo', 'github.com/gofiber/', 'github.com/go-chi/', 'github.com/gorilla/'), ...D('tech', 'net/http', 'database/sql', 'gorm.io/', 'github.com/jackc/pgx', 'go.mongodb.org/', 'github.com/redis/', 'github.com/segmentio/kafka-go', 'github.com/IBM/sarama', 'github.com/Shopify/sarama')],
  php: [...D('framework', 'Symfony\\', 'Illuminate\\', 'Laravel\\'), ...D('tech', 'Doctrine\\', 'GuzzleHttp\\')],
  cs: [...D('framework', 'Microsoft.AspNetCore'), ...D('tech', 'Microsoft.EntityFrameworkCore', 'System.Data', 'Dapper', 'Npgsql', 'MongoDB.', 'StackExchange.Redis', 'Confluent.Kafka')],
  py: [...D('framework', 'django', 'flask', 'fastapi', 'pydantic'), ...D('tech', 'sqlalchemy', 'requests', 'httpx', 'psycopg', 'pymongo', 'redis', 'boto3', 'celery', 'kafka')],
  dart: [...D('framework', 'package:flutter/'), ...D('tech', 'dart:io', 'package:dio/', 'package:http/', 'package:sqflite', 'package:drift', 'package:firebase')],
};
const matchesPrefix = (spec, prefix) => spec === prefix || spec.startsWith(prefix) && (/[/\\.:]$/.test(prefix) || /^[/\\.:-]/.test(spec.slice(prefix.length)));
export const denyHit = (spec, lang) => DENY[lang]?.find((d) => matchesPrefix(spec, d.p));

// ---------------------------------------------------------------- scan the tree
export function scanTree(root) {
  const files = [];
  const dirs = new Set();
  const manifests = [];
  let truncated = false;
  const walk = (d, depth) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (files.length >= MAX_FILES) { truncated = true; return; }
      const full = join(d, e.name);
      const rel = relative(root, full).split(sep).join('/');
      if (e.isDirectory()) {
        if (SKIP_DIRS.has(e.name) || (e.name.startsWith('.') && e.name !== '.claude-plugin')) continue;
        dirs.add(rel);
        if (depth < 12) walk(full, depth + 1);
      } else if (e.isFile()) {
        if (depth <= 3 && /^(package\.json|pom\.xml|build\.gradle(\.kts)?|go\.mod|composer\.json|pubspec\.yaml|pyproject\.toml|requirements\.txt|setup\.py|plugin\.json|serverless\.yml|serverless\.yaml|template\.yaml|samconfig\.toml|.*\.csproj)$/.test(e.name)) manifests.push(rel);
        const lang = LANG[extname(e.name)];
        if (lang) files.push({ rel, full, lang });
      }
    }
  };
  walk(root, 0);
  return { root, files, dirs, manifests, truncated };
}

function stacksOf(model) {
  const found = new Map();
  const note = (name, via) => found.set(name, [...(found.get(name) ?? []), via]);
  for (const m of model.manifests) {
    const text = (() => { try { return readFileSync(join(model.root, m), 'utf8'); } catch { return ''; } })();
    const name = basename(m);
    if (name === 'package.json') note(/@nestjs\/core/.test(text) ? 'node (NestJS)' : /"fastify"/.test(text) ? 'node (Fastify)' : /"express"/.test(text) ? 'node (Express)' : 'node/typescript', m);
    else if (name === 'pom.xml' || name.startsWith('build.gradle')) note(/spring-boot/.test(text) ? 'java/kotlin (Spring Boot)' : 'java/kotlin', m);
    else if (name === 'go.mod') note('go', m);
    else if (name === 'composer.json') note(/symfony/.test(text) ? 'php (Symfony)' : /laravel/.test(text) ? 'php (Laravel)' : 'php', m);
    else if (name.endsWith('.csproj')) note('dotnet', m);
    else if (name === 'pubspec.yaml') note(/flutter/.test(text) ? 'dart (Flutter)' : 'dart', m);
    else if (/^(pyproject\.toml|requirements\.txt|setup\.py)$/.test(name)) note(/fastapi/i.test(text) ? 'python (FastAPI)' : /django/i.test(text) ? 'python (Django)' : /flask/i.test(text) ? 'python (Flask)' : 'python', m);
    else if (name === 'plugin.json') note('claude-code plugin', m);
    else if (/^(serverless\.ya?ml|template\.yaml|samconfig\.toml)$/.test(name)) note('serverless', m);
  }
  return [...found].map(([stack, via]) => ({ stack, via: via.slice(0, 3) }));
}

// ---------------------------------------------------------------- detect
const has = (set, ...names) => names.filter((n) => [...set].some((d) => d.split('/').includes(n)));

export function detect(model) {
  const segs = new Set();
  for (const d of model.dirs) for (const s of d.split('/')) segs.add(s.toLowerCase());
  const dirList = [...model.dirs].map((d) => d.toLowerCase());
  const fileNames = model.files.map((f) => basename(f.rel).toLowerCase());
  const ev = {};
  const add = (style, points, why) => { (ev[style] ??= { score: 0, evidence: [] }); ev[style].score += points; ev[style].evidence.push(why); };
  const firstDir = (word) => [...model.dirs].find((d) => d.toLowerCase().split('/').includes(word));

  const portsDirs = has(segs, 'ports', 'port');
  const adaptersDirs = has(segs, 'adapters', 'adapter');
  if (portsDirs.length && adaptersDirs.length) add('hexagonal', 5, `ports and adapters folders (${firstDir(portsDirs[0])}, ${firstDir(adaptersDirs[0])})`);
  else if (adaptersDirs.length) add('hexagonal', 1, `adapters folder (${firstDir(adaptersDirs[0])})`);
  const dirs2 = has(segs, 'inbound', 'outbound', 'driving', 'driven', 'primary', 'secondary');
  if (dirs2.length >= 2) add('hexagonal', 2, `inbound and outbound style folders (${dirs2.join(', ')})`);

  const cleanWords = has(segs, 'usecases', 'use-cases', 'use_cases', 'interactors', 'presenters', 'gateways', 'entities', 'interface-adapters', 'interface_adapters');
  if (cleanWords.length >= 3) add('clean', 5, `clean-architecture folders (${cleanWords.join(', ')})`);
  else if (cleanWords.length === 2) add('clean', 2, `some clean-architecture folders (${cleanWords.join(', ')})`);

  if (dirList.some((d) => /(^|\/)core\/domain$/.test(d)) && dirList.some((d) => /(^|\/)core\/application$/.test(d))) add('onion', 4, 'core/domain and core/application modules');
  if (segs.has('composition') && segs.has('infrastructure')) add('onion', 2, 'composition and infrastructure modules');

  const four = has(segs, 'domain', 'application', 'infrastructure').length + (has(segs, 'interface', 'interfaces', 'presentation').length ? 1 : 0);
  if (four >= 4) add('layered (DDD four-layer)', 5, 'interface or presentation, application, domain and infrastructure folders');
  else if (four === 3) add('layered (DDD four-layer)', 3, 'three of the four DDD layers present');
  const trad = has(segs, 'controllers', 'services', 'repositories', 'dao').length + (has(segs, 'models', 'entities').length ? 1 : 0);
  if (trad >= 3) add('layered (traditional)', 4, 'controllers, services, repositories and models folders (technical roles at the top)');

  const cola = [...segs].filter((s) => COLA_SUFFIX.some(([suf]) => s.endsWith(suf)) || s.endsWith('-client'));
  if (cola.length >= 3) add('cola', 5, `COLA-style modules (${cola.slice(0, 5).join(', ')})`);

  const featureRoot = [...model.dirs].find((d) => /(^|\/)(features|slices)$/i.test(d));
  if (featureRoot) {
    const kids = [...model.dirs].filter((d) => d.startsWith(`${featureRoot}/`) && d.split('/').length === featureRoot.split('/').length + 1);
    if (kids.length >= 2) add('vertical slice', 4, `feature folders under ${featureRoot} (${kids.length} features)`);
    const ops = [...model.dirs].filter((d) => d.startsWith(`${featureRoot}/`) && d.split('/').length === featureRoot.split('/').length + 2);
    if (ops.length >= 3) add('vertical slice', 1, 'operation folders inside features');
  }

  if (has(segs, 'commands').length && has(segs, 'queries').length) add('cqrs', 4, 'commands and queries folders');
  const cmdFiles = fileNames.filter((n) => /(command|query)(handler)?\./.test(n)).length;
  if (cmdFiles >= 3) add('cqrs', 2, `${cmdFiles} command or query files`);
  if (has(segs, 'readmodels', 'read_models', 'projections').length) add('cqrs', 1, 'read models or projections');

  const esDirs = has(segs, 'eventstore', 'event_store', 'event-store', 'snapshots');
  if (esDirs.length) add('event sourcing', 4, `event store or snapshot folders (${esDirs.join(', ')})`);
  if (has(segs, 'events').length && has(segs, 'projections').length) add('event sourcing', 2, 'events and projections folders');
  if (fileNames.filter((n) => /(eventstore|projection)/.test(n)).length >= 2) add('event sourcing', 1, 'event store or projection files');

  const msgDirs = has(segs, 'consumers', 'producers', 'subscribers', 'publishers', 'outbox', 'messaging', 'listeners');
  if (msgDirs.length) add('event-driven', 2 + (msgDirs.includes('outbox') ? 2 : 0), `messaging folders (${msgDirs.join(', ')})`);
  if (fileNames.some((n) => n.includes('outbox'))) add('event-driven', 2, 'outbox files');
  if (model.manifests.some((m) => { try { return /kafka|rabbit|amqp|nats/i.test(readFileSync(join(model.root, m), 'utf8')); } catch { return false; } })) add('event-driven', 1, 'a message-broker dependency in a manifest');

  if (model.manifests.some((m) => m.endsWith('.claude-plugin/plugin.json') || m.endsWith('plugin.json')) && has(segs, '.claude-plugin', 'skills', 'commands', 'agents', 'hooks').length) add('plugin', 4, 'a plugin manifest with component folders');
  if (has(segs, 'systems').length && has(segs, 'components').length) add('game', 2, 'systems and components folders');
  if (fileNames.some((n) => /statemachine|objectpool/.test(n))) add('game', 2, 'state machine or object pool files');

  const moduleRoot = [...model.dirs].find((d) => /^(modules|bounded-contexts)$/i.test(d) || /(^|\/)(modules|bounded-contexts)$/i.test(d) && d.split('/').length <= 2);
  if (moduleRoot) {
    const kids = [...model.dirs].filter((d) => d.startsWith(`${moduleRoot}/`) && d.split('/').length === moduleRoot.split('/').length + 1);
    if (kids.length >= 2) add('modular monolith', 4, `module folders under ${moduleRoot} (${kids.length} modules)`);
  }

  const svcRoot = [...model.dirs].find((d) => /^services$/i.test(d));
  if (svcRoot) {
    const kids = [...model.dirs].filter((d) => d.startsWith(`${svcRoot}/`) && d.split('/').length === svcRoot.split('/').length + 1);
    if (kids.length >= 4) add('microservices', 4, `top-level services/ with ${kids.length} children`);
    else if (kids.length >= 2) add('service-based', 3, `top-level services/ with ${kids.length} coarse children`);
  }

  if (has(segs, 'functions', 'lambdas').length) add('serverless', 3, `function folders (${has(segs, 'functions', 'lambdas').join(', ')})`);
  if (model.manifests.some((m) => /serverless\.ya?ml$|template\.yaml$|samconfig\.toml$/i.test(m))) add('serverless', 3, 'a serverless or SAM manifest');

  const pipeWords = has(segs, 'filters', 'pipes', 'pipelines', 'stages');
  if (pipeWords.length >= 2) add('pipeline', 3, `pipeline folders (${pipeWords.join(', ')})`);

  if (has(segs, 'shell').length && dirList.some((d) => /(^|\/)core$/.test(d))) add('functional core', 3, 'core/ next to shell/');

  if (has(segs, 'plugins', 'extensions').length && has(segs, 'kernel', 'host').length) add('microkernel', 4, 'kernel or host plus plugins');

  if ((has(segs, 'client').length && has(segs, 'server').length) || (has(segs, 'frontend').length && has(segs, 'backend').length)) add('client-server', 2, 'separate client and server (or frontend and backend) folders');

  if (has(segs, 'processing-units', 'processing_units', 'datagrid', 'data-grid', 'data_grid').length) add('space-based', 4, 'processing-unit or data-grid folders');

  // Dependency direction raises or lowers confidence of the domain-centric styles.
  const violations = check(model).violations;
  const domainFiles = model.files.filter((f) => classifySegments(f.rel.split('/').slice(0, -1), f.lang) === 'domain').length;
  const critical = violations.filter((v) => v.severity === 'critical').length;
  const direction = { domainFiles, critical, candidates: violations.length };
  const centric = ['hexagonal', 'clean', 'onion', 'layered (DDD four-layer)', 'cola'];
  for (const s of centric) {
    if (!ev[s]) continue;
    if (domainFiles > 0 && critical === 0) { ev[s].score += 2; ev[s].evidence.push('no domain or application file imports an outer layer'); }
    else if (critical > 0) { ev[s].score -= 2; ev[s].evidence.push(`${critical} imports point outward: the structure may be nominal`); }
  }

  const ranked = Object.entries(ev).map(([name, v]) => ({ name, score: v.score, evidence: v.evidence })).filter((s) => s.score > 0).sort((a, b) => b.score - a.score);
  const top = ranked[0];
  const margin = top ? top.score - (ranked[1]?.score ?? 0) : 0;
  for (const s of ranked) s.confidence = s.score >= 6 && (s === top ? margin >= 2 || ranked.length === 1 : true) ? 'high' : s.score >= 3 ? 'medium' : 'low';
  return {
    root: model.root,
    stacks: stacksOf(model),
    languages: Object.entries(model.files.reduce((a, f) => ({ ...a, [f.lang]: (a[f.lang] ?? 0) + 1 }), {})).map(([lang, files]) => ({ lang, files })),
    files: model.files.length,
    truncated: model.truncated,
    styles: ranked,
    verdict: !top || top.score < 3 ? 'unclear' : top.name,
    direction,
  };
}

// ---------------------------------------------------------------- check
export function check(model) {
  const violations = [];
  const goModule = (() => { try { return readFileSync(join(model.root, 'go.mod'), 'utf8').match(/^module\s+(\S+)/m)?.[1] ?? ''; } catch { return ''; } })();
  const pubspec = (() => { try { return readFileSync(join(model.root, 'pubspec.yaml'), 'utf8').match(/^name:\s*(\S+)/m)?.[1] ?? ''; } catch { return ''; } })();
  const pyRoots = new Set();
  for (const base of ['', 'src']) {
    const dir = join(model.root, base);
    if (!existsSync(dir)) continue;
    for (const e of readdirSync(dir, { withFileTypes: true })) if (e.isDirectory() && !SKIP_DIRS.has(e.name) && !e.name.startsWith('.')) pyRoots.add(e.name);
  }

  for (const f of model.files) {
    const segs = f.rel.split('/');
    const dirSegs = segs.slice(0, -1);
    if (isTestPath(segs)) continue;
    let text;
    try { if (statSync(f.full).size > MAX_BYTES) continue; text = readFileSync(f.full, 'utf8'); } catch { continue; }
    const layer = classifySegments(dirSegs, f.lang);
    const feature = f.rel.match(/(?:^|\/)(?:features|slices)\/([^/]+)\//i)?.[1];
    const ns = ownNamespace(text, f.lang);
    const nsRoot = f.lang === 'java' ? ns.split('.').slice(0, 2).join('.') : f.lang === 'php' ? ns.split('\\')[0] : ns.split('.')[0];

    for (const imp of extractImports(text, f.lang)) {
      const spec = imp.spec;
      const internal =
        f.lang === 'ts' ? /^(\.|@\/|~\/|src\/|#)/.test(spec)
        : f.lang === 'java' ? Boolean(nsRoot) && spec.startsWith(`${nsRoot}.`)
        : f.lang === 'go' ? Boolean(goModule) && spec.startsWith(goModule)
        : f.lang === 'php' ? Boolean(nsRoot) && spec.split('\\')[0] === nsRoot
        : f.lang === 'cs' ? Boolean(nsRoot) && spec.split('.')[0] === nsRoot
        : f.lang === 'py' ? spec.startsWith('.') || pyRoots.has(spec.split('.')[0])
        : spec.startsWith('.') || (Boolean(pubspec) && spec.startsWith(`package:${pubspec}/`));
      const add = (severity, rule, message) => violations.push({ severity, rule, file: f.rel, line: imp.line, message, import: spec });

      if (!internal) {
        const hit = denyHit(spec, f.lang);
        if (hit && layer === 'domain') add('warning', 'framework-in-core', `domain imports ${hit.kind === 'framework' ? 'a framework' : 'a database, HTTP or broker client'} (${spec})`);
        else if (hit && hit.kind === 'tech' && layer === 'application') add('warning', 'technology-in-application', `application layer imports a technology client (${spec}); put it behind a port`);
        continue;
      }
      let targetSegs;
      if (f.lang === 'ts' || f.lang === 'dart' || (f.lang === 'py' && spec.startsWith('.'))) {
        const clean = spec.replace(/^package:[^/]+\//, '');
        targetSegs = spec.startsWith('.') && f.lang !== 'py' ? posix.normalize(posix.join(posix.dirname(f.rel), clean)).split('/') : clean.split(/[/.]/);
      } else targetSegs = spec.split(/[./\\:]/);
      const targetLayer = classifySegments(targetSegs, f.lang);
      if (layer === 'domain' && targetLayer && targetLayer !== 'domain' && targetLayer !== 'composition') add('critical', 'core-depends-on-outer', `domain imports the ${targetLayer} layer (${spec})`);
      else if (layer === 'application' && (targetLayer === 'infrastructure' || targetLayer === 'presentation')) add('critical', 'core-depends-on-outer', `application imports the ${targetLayer} layer (${spec})`);
      else if (layer === 'presentation' && /(^|[/.\\])(persistence|repositories|repository|dao|postgres|mysql|mongo|sql|database)([/.\\]|$)/i.test(spec) && targetLayer !== 'domain' && targetLayer !== 'application') add('warning', 'adapter-without-port', `a delivery-layer file imports persistence directly (${spec}); go through a use case`);
      if (feature) {
        const other = (f.lang === 'ts' && spec.startsWith('.') ? posix.normalize(posix.join(posix.dirname(f.rel), spec)) : spec).match(/(?:^|[/.\\])(?:features|slices)[/.\\]([^/.\\]+)/i)?.[1];
        if (other && other.toLowerCase() !== feature.toLowerCase()) add('warning', 'cross-feature-import', `feature "${feature}" imports feature "${other}" (${spec}); use its public entry point or an event`);
      }
    }
  }
  const order = { critical: 0, warning: 1, info: 2 };
  violations.sort((a, b) => order[a.severity] - order[b.severity] || a.file.localeCompare(b.file) || a.line - b.line);
  return { root: model.root, files: model.files.length, truncated: model.truncated, violations };
}

// ---------------------------------------------------------------- CLI
function main() {
  const args = process.argv.slice(2);
  const [command, dir] = args.filter((a) => !a.startsWith('--'));
  const json = args.includes('--json');
  if (!['detect', 'check'].includes(command) || !dir) {
    console.error('usage: arch-scan.mjs detect|check <dir> [--json] [--all]');
    process.exit(2);
  }
  let model;
  try {
    if (!statSync(dir).isDirectory()) throw new Error('not a directory');
    model = scanTree(dir);
  } catch (e) {
    console.error(`arch-scan: cannot read ${dir}: ${e.message}`);
    process.exit(2);
  }
  if (command === 'detect') {
    const r = detect(model);
    if (json) return console.log(JSON.stringify(r, null, 2));
    console.log(`Root: ${r.root}   Files scanned: ${r.files}${r.truncated ? ' (truncated)' : ''}`);
    console.log(`Stack: ${r.stacks.map((s) => s.stack).join(', ') || 'not recognized'}`);
    console.log(`Languages: ${r.languages.map((l) => `${l.lang} ${l.files}`).join(', ') || 'none'}`);
    console.log(`Verdict: ${r.verdict}${r.styles[0] ? ` (${r.styles[0].confidence}, score ${r.styles[0].score})` : ''}`);
    for (const s of r.styles) { console.log(`  ${s.name} [${s.confidence}, ${s.score}]`); for (const w of s.evidence) console.log(`    - ${w}`); }
    console.log(`Direction: ${r.direction.domainFiles} domain files, ${r.direction.critical} critical outward imports, ${r.direction.candidates} candidates in total`);
    console.log(`Next: node scripts/arch-scan.mjs check ${dir}   (candidates are places to look, not findings)`);
    return;
  }
  const r = check(model);
  if (json) return console.log(JSON.stringify(r, null, 2));
  const shown = args.includes('--all') ? r.violations : r.violations.slice(0, 60);
  for (const v of shown) console.log(`${v.severity.padEnd(8)} ${v.file}:${v.line}  [${v.rule}] ${v.message}`);
  if (shown.length < r.violations.length) console.log(`... ${r.violations.length - shown.length} more (use --all)`);
  const count = (s) => r.violations.filter((v) => v.severity === s).length;
  console.log(`${r.violations.length} candidate(s) in ${r.files} files: ${count('critical')} critical, ${count('warning')} warning. Confirm each by reading the code.`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
