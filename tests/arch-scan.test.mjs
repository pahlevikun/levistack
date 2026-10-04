import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { check, classifySegments, denyHit, detect, extractImports, scanTree } from '../skills/architecture/super-architecture/scripts/arch-scan.mjs';

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), '../skills/architecture/super-architecture/scripts/arch-scan.mjs');

function tree(files) {
  const root = mkdtempSync(join(tmpdir(), 'arch-scan-'));
  for (const [rel, content] of Object.entries(files)) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, content);
  }
  return root;
}
const rules = (root) => check(scanTree(root)).violations.map((v) => `${v.rule}:${v.file}`);

test('classifySegments: deepest layer word wins, ports belong to the inside, Maven src/main is not a composition root', () => {
  assert.equal(classifySegments(['src', 'orders', 'domain']), 'domain');
  assert.equal(classifySegments(['adapters', 'inbound', 'http']), 'presentation');
  assert.equal(classifySegments(['adapters', 'outbound', 'persistence']), 'infrastructure');
  assert.equal(classifySegments(['application', 'ports', 'outbound']), 'application');
  assert.equal(classifySegments(['domain', 'ports', 'out']), 'domain');
  assert.equal(classifySegments(['order-domain', 'src', 'main', 'java', 'com', 'acme', 'domain'], 'java'), 'domain');
  assert.equal(classifySegments(['cmd', 'api']), 'composition');
  assert.equal(classifySegments(['com', 'acme', 'order', 'app'], 'java'), 'application');
  assert.equal(classifySegments(['utils']), null);
});

test('extractImports reads each language and reports line numbers', () => {
  const ts = "import a from './a';\nimport {\n  b,\n} from '../b';\nconst c = require('c');\nawait import('d');\n";
  assert.deepEqual(extractImports(ts, 'ts').map((i) => [i.spec, i.line]), [['./a', 1], ['../b', 2], ['c', 5], ['d', 6]]);
  assert.deepEqual(extractImports('package x;\nimport static a.b.C;\nimport d.e.*;', 'java').map((i) => i.spec), ['a.b.C', 'd.e.*']);
  assert.deepEqual(extractImports('import (\n  "net/http"\n  x "github.com/acme/app/internal/domain"\n)\nimport "fmt"', 'go').map((i) => i.spec).sort(), ['fmt', 'github.com/acme/app/internal/domain', 'net/http']);
  assert.deepEqual(extractImports('use App\\Domain\\Order;\nuse Symfony\\Component\\X as Y;', 'php').map((i) => i.spec), ['App\\Domain\\Order', 'Symfony\\Component\\X']);
  assert.deepEqual(extractImports('using System.Linq;\nusing static Acme.Util;', 'cs').map((i) => i.spec), ['System.Linq', 'Acme.Util']);
  assert.deepEqual(extractImports('from .a import b\nimport os.path\nfrom app.domain import x', 'py').map((i) => i.spec), ['.a', 'os.path', 'app.domain']);
  assert.deepEqual(extractImports("import 'package:app/domain/x.dart';\nexport './y.dart';", 'dart').map((i) => i.spec), ['package:app/domain/x.dart', './y.dart']);
});

test('denyHit matches prefixes on word boundaries only', () => {
  assert.equal(denyHit('express', 'ts')?.kind, 'framework');
  assert.equal(denyHit('react-dom', 'ts')?.kind, 'framework');
  assert.equal(denyHit('prisma', 'ts')?.kind, 'tech');
  assert.equal(denyHit('pgsomething', 'ts'), undefined);
  assert.equal(denyHit('org.springframework.stereotype.Service', 'java')?.kind, 'framework');
  assert.equal(denyHit('org.springframework.data.jpa.Repository', 'java')?.kind, 'framework'); // first match wins
  assert.equal(denyHit('net/http', 'go')?.kind, 'tech');
  assert.equal(denyHit('internal/domain', 'go'), undefined);
});

test('check: a clean hexagonal tree has no candidates, including use cases importing their own ports', () => {
  const root = tree({
    'src/orders/domain/order.ts': 'export class Order {}\n',
    'src/orders/application/ports/outbound/repo.ts': "import { Order } from '../../../domain/order';\nexport interface Repo {}\n",
    'src/orders/application/usecases/place.ts': "import { Order } from '../../domain/order';\nimport { Repo } from '../ports/outbound/repo';\n",
    'src/orders/adapters/outbound/persistence/pg.ts': "import { Repo } from '../../../application/ports/outbound/repo';\nimport pg from 'pg';\n",
    'src/orders/adapters/inbound/http/controller.ts': "import { PlaceOrder } from '../../../application/usecases/place';\nimport express from 'express';\n",
  });
  try {
    assert.deepEqual(rules(root), []);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('check: outward imports, framework leaks and controllers touching persistence are flagged; tests are ignored', () => {
  const root = tree({
    'src/domain/order.ts': "import express from 'express';\nimport { Pg } from '../infrastructure/pg';\n",
    'src/application/place.ts': "import { Pg } from '../infrastructure/pg';\nimport axios from 'axios';\n",
    'src/infrastructure/pg.ts': 'export class Pg {}\n',
    'src/presentation/controllers/order.ts': "import { Repo } from '../../persistence/repo';\n",
    'src/persistence/repo.ts': 'export class Repo {}\n',
    'src/domain/__tests__/order.test.ts': "import { Pg } from '../../infrastructure/pg';\n",
  });
  try {
    const got = rules(root);
    assert.ok(got.includes('core-depends-on-outer:src/domain/order.ts'));
    assert.ok(got.includes('framework-in-core:src/domain/order.ts'));
    assert.ok(got.includes('core-depends-on-outer:src/application/place.ts'));
    assert.ok(got.includes('technology-in-application:src/application/place.ts'));
    assert.ok(got.includes('adapter-without-port:src/presentation/controllers/order.ts'));
    assert.ok(!got.some((r) => r.includes('__tests__')));
    const first = check(scanTree(root)).violations[0];
    assert.equal(first.severity, 'critical');
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('check: Java packages, Go module paths and a Maven src/main layout', () => {
  const root = tree({
    'go.mod': 'module github.com/acme/app\n',
    'internal/domain/order.go': 'package domain\nimport (\n  "net/http"\n  "github.com/acme/app/internal/adapters/pg"\n)\n',
    'order-domain/src/main/java/com/acme/order/domain/Order.java': 'package com.acme.order.domain;\nimport org.springframework.stereotype.Service;\nimport com.acme.order.app.Exec;\n',
  });
  try {
    const got = rules(root);
    assert.ok(got.includes('framework-in-core:internal/domain/order.go'));
    assert.ok(got.includes('core-depends-on-outer:internal/domain/order.go'));
    assert.ok(got.includes('framework-in-core:order-domain/src/main/java/com/acme/order/domain/Order.java'));
    assert.ok(got.includes('core-depends-on-outer:order-domain/src/main/java/com/acme/order/domain/Order.java'));
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('check: cross-feature imports are flagged in feature-first trees', () => {
  const root = tree({
    'features/orders/place/handler.ts': "import { x } from '../../billing/charge/handler';\nimport { y } from './local';\n",
    'features/orders/place/local.ts': 'export const y = 1;\n',
    'features/billing/charge/handler.ts': 'export const x = 1;\n',
  });
  try {
    assert.deepEqual(rules(root), ['cross-feature-import:features/orders/place/handler.ts']);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('detect: names the dominant style with evidence and lowers confidence when the direction is violated', () => {
  const clean = tree({
    'src/orders/domain/order.ts': 'export class Order {}\n',
    'src/orders/application/ports/outbound/repo.ts': 'export interface Repo {}\n',
    'src/orders/application/usecases/place.ts': "import { Order } from '../../domain/order';\n",
    'src/orders/adapters/inbound/http/c.ts': 'export const c = 1;\n',
    'src/orders/adapters/outbound/persistence/pg.ts': 'export const p = 1;\n',
    'package.json': '{"dependencies":{"express":"4"}}',
  });
  const bad = tree({
    'src/domain/order.ts': "import { Pg } from '../adapters/outbound/pg';\n",
    'src/application/ports/x.ts': 'export interface X {}\n',
    'src/adapters/inbound/c.ts': 'export const c = 1;\n',
    'src/adapters/outbound/pg.ts': 'export class Pg {}\n',
  });
  try {
    const a = detect(scanTree(clean));
    assert.equal(a.verdict, 'hexagonal');
    assert.equal(a.styles[0].confidence, 'high');
    assert.ok(a.stacks.some((s) => s.stack.includes('Express')));
    const b = detect(scanTree(bad));
    assert.equal(b.verdict, 'hexagonal');
    assert.ok(b.styles[0].score < a.styles[0].score);
    assert.ok(b.styles[0].evidence.some((e) => /point outward/.test(e)));
  } finally { rmSync(clean, { recursive: true, force: true }); rmSync(bad, { recursive: true, force: true }); }
});

test('detect: recognizes vertical slice, COLA, CQRS and says unclear when there is no signal', () => {
  const vsa = tree({ 'features/a/x/h.ts': '', 'features/b/y/h.ts': '', 'features/c/z/h.ts': '' });
  const cola = tree({ 'shop-adapter/A.java': '', 'shop-app/B.java': '', 'shop-domain/C.java': '', 'shop-infrastructure/D.java': '' });
  const cq = tree({ 'src/commands/place-order.command.ts': '', 'src/commands/place-order.command-handler.ts': '', 'src/queries/get-order.query.ts': '' });
  const none = tree({ 'src/utils/a.ts': '', 'src/lib/b.ts': '' });
  try {
    assert.equal(detect(scanTree(vsa)).verdict, 'vertical slice');
    assert.equal(detect(scanTree(cola)).verdict, 'cola');
    assert.ok(detect(scanTree(cq)).styles.some((s) => s.name === 'cqrs'));
    assert.equal(detect(scanTree(none)).verdict, 'unclear');
  } finally { for (const r of [vsa, cola, cq, none]) rmSync(r, { recursive: true, force: true }); }
});

test('detect: names modular monolith, serverless, microkernel and pipeline', () => {
  const mods = tree({ 'modules/ordering/a.ts': '', 'modules/billing/b.ts': '' });
  const sls = tree({ 'functions/checkout/h.ts': '', 'serverless.yml': 'service: shop\n' });
  const mk = tree({ 'kernel/boot.ts': '', 'plugins/search/p.ts': '' });
  const pipe = tree({ 'filters/clean/f.ts': '', 'pipes/queue.ts': '' });
  try {
    assert.equal(detect(scanTree(mods)).verdict, 'modular monolith');
    assert.equal(detect(scanTree(sls)).verdict, 'serverless');
    assert.equal(detect(scanTree(mk)).verdict, 'microkernel');
    assert.equal(detect(scanTree(pipe)).verdict, 'pipeline');
  } finally { for (const r of [mods, sls, mk, pipe]) rmSync(r, { recursive: true, force: true }); }
});

test('CLI: json output parses, and bad usage exits 2', () => {
  const root = tree({ 'src/domain/o.ts': "import express from 'express';\n" });
  try {
    const ok = spawnSync(process.execPath, [SCRIPT, 'check', root, '--json'], { encoding: 'utf8' });
    assert.equal(ok.status, 0);
    assert.equal(JSON.parse(ok.stdout).violations[0].rule, 'framework-in-core');
    assert.equal(spawnSync(process.execPath, [SCRIPT, 'nope', root], { encoding: 'utf8' }).status, 2);
    assert.equal(spawnSync(process.execPath, [SCRIPT, 'detect', join(root, 'missing')], { encoding: 'utf8' }).status, 2);
  } finally { rmSync(root, { recursive: true, force: true }); }
});
