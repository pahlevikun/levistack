import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { detect, scan } from '../skills/engineering/super-elixir/scripts/elixir-scan.mjs';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const script = join(repo, 'skills/engineering/super-elixir/scripts/elixir-scan.mjs');

function project(files) {
  const root = mkdtempSync(join(tmpdir(), 'elixir-scan-'));
  for (const [rel, content] of Object.entries(files)) {
    const p = join(root, rel);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, content);
  }
  return root;
}
const done = (r) => rmSync(r, { recursive: true, force: true });
const ids = (r) => r.candidates.map((c) => c.id);

test('scan: flags the risky patterns with file, line and the guide to read', () => {
  const root = project({
    'lib/a.ex': [
      'defmodule A do',
      '  def run(input) do',
      '    Code.eval_string(input)',
      '    :erlang.binary_to_term(input)',
      '    String.to_atom(input)',
      '    Repo.query!("SELECT * FROM t WHERE id = #{input}")',
      '    spawn(fn -> :ok end)',
      '    IO.inspect(input)',
      '    Logger.info("got #{inspect(params)}")',
      '  end',
      'end',
    ].join('\n'),
  });
  try {
    const r = scan(root);
    for (const id of ['SEC001', 'SEC002', 'SEC003', 'SEC004', 'OTP001', 'CODE002', 'SEC009']) assert.ok(ids(r).includes(id), id);
    const eval_ = r.candidates.find((c) => c.id === 'SEC001');
    assert.equal(eval_.file, 'lib/a.ex');
    assert.equal(eval_.line, 3);
    assert.match(eval_.guide, /code-injection\.md$/);
    assert.equal(r.candidates[0].severity, 'critical');
  } finally {
    done(root);
  }
});

test('scan: leaves safe code alone', () => {
  const root = project({
    'lib/safe.ex': [
      'defmodule Safe do',
      '  # Code.eval_string(x) is only in a comment',
      '  def a(x), do: String.to_atom("literal")',
      '  def b(x), do: String.to_existing_atom(x)',
      '  def c(x), do: :erlang.binary_to_term(x, [:safe])',
      '  @doc """',
      '      iex> String.to_atom(x)',
      '  """',
      '  def d, do: Task.Supervisor.start_child(S, fn -> :ok end)',
      'end',
    ].join('\n'),
  });
  try {
    assert.deepEqual(scan(root).candidates, []);
  } finally {
    done(root);
  }
});

test('scan: test files skip the security rules but still flag Process.sleep', () => {
  const root = project({
    'test/a_test.exs': 'defmodule ATest do\n  test "x" do\n    Code.eval_string("1")\n    Process.sleep(100)\n  end\nend\n',
  });
  try {
    assert.deepEqual(ids(scan(root)), ['CODE003']);
  } finally {
    done(root);
  }
});

test('scan: compile-time config secrets are flagged, runtime.exs and test.exs are not', () => {
  const root = project({
    'config/prod.exs': 'import Config\nconfig :app, secret_key_base: "abcdefghijklmnopqrstuvwxyz"\n',
    'config/runtime.exs': 'import Config\nconfig :app, secret_key_base: System.fetch_env!("KEY")\n',
    'config/test.exs': 'import Config\nconfig :app, password: "dummy-password-here"\n',
  });
  try {
    const r = scan(root);
    assert.deepEqual(r.candidates.map((c) => `${c.id}@${c.file}`), ['SEC007@config/prod.exs']);
  } finally {
    done(root);
  }
});

test('scan: finds blocking work in a GenServer callback and a = step in with', () => {
  const root = project({
    'lib/s.ex': [
      'defmodule S do',
      '  use GenServer',
      '  def handle_call(:x, _from, state) do',
      '    Req.get!("http://example.com")',
      '    {:reply, :ok, state}',
      '  end',
      '  def run(id) do',
      '    with {:ok, a} <- fetch(id),',
      '         b = parse(a),',
      '         {:ok, c} <- save(b) do',
      '      c',
      '    end',
      '  end',
      'end',
    ].join('\n'),
  });
  try {
    const r = scan(root);
    assert.ok(ids(r).includes('PERF002'));
    const w = r.candidates.find((c) => c.id === 'CODE001');
    assert.equal(w.line, 9);
  } finally {
    done(root);
  }
});

test('scan: skips deps and _build', () => {
  const root = project({ 'deps/x/lib/x.ex': 'Code.eval_string("1")\n', '_build/dev/lib/y.ex': 'Code.eval_string("1")\n' });
  try {
    assert.equal(scan(root).filesScanned, 0);
  } finally {
    done(root);
  }
});

test('detect: reads mix.exs and reports gates the project really has', () => {
  const root = project({
    'mix.exs': 'defmodule App.MixProject do\n  def project, do: [app: :app, elixir: "~> 1.18", deps: deps()]\n  defp deps, do: [{:phoenix, "~> 1.7"}, {:ecto_sql, "~> 3.11"}, {:credo, "~> 1.7", only: :dev}]\nend\n',
    'mix.lock': '%{}\n',
    'lib/s.ex': 'defmodule S do\n  use GenServer\nend\n',
    'lib/u.ex': 'defmodule U do\n  use Ecto.Schema\nend\n',
    'test/s_test.exs': 'defmodule STest do\nend\n',
  });
  try {
    const d = detect(root);
    assert.equal(d.kind, 'phoenix');
    assert.equal(d.elixir.requirement, '~> 1.18');
    assert.equal(d.counts.genServers, 1);
    assert.equal(d.counts.schemas, 1);
    assert.equal(d.counts.testFiles, 1);
    assert.ok(d.gates.includes('mix credo --strict'));
    assert.ok(!d.gates.includes('mix sobelow'), 'no sobelow dep, so no sobelow gate');
    assert.ok(!d.gates.includes('mix dialyzer'));
    assert.deepEqual(d.reviewPasses, ['code-review', 'antipatterns', 'security-review', 'performance-review']);
    assert.ok(d.specialities.includes('otp') && d.specialities.includes('ecto'));
  } finally {
    done(root);
  }
});

test('detect: umbrella apps are merged and a plain folder reports no mix.exs', () => {
  const umbrella = project({ 'mix.exs': 'defmodule U.MixProject do\nend\n', 'apps/a/mix.exs': 'defmodule A do\n  defp deps, do: [{:oban, "~> 2.0"}]\nend\n', 'apps/b/mix.exs': 'defmodule B do\nend\n' });
  const plain = project({ 'README.md': '# hi\n' });
  try {
    assert.equal(detect(umbrella).kind, 'umbrella');
    assert.ok(detect(umbrella).deps.includes('oban'));
    assert.equal(detect(plain).kind, 'no mix.exs found');
    assert.deepEqual(detect(plain).gates, []);
  } finally {
    done(umbrella);
    done(plain);
  }
});

test('cli: json output, strict exit code, and usage error', () => {
  const root = project({ 'lib/a.ex': 'Code.eval_string(x)\n' });
  try {
    const ok = spawnSync('node', [script, 'scan', root, '--json'], { encoding: 'utf8' });
    assert.equal(ok.status, 0);
    assert.equal(JSON.parse(ok.stdout).candidates[0].id, 'SEC001');
    assert.equal(spawnSync('node', [script, 'scan', root, '--strict'], { encoding: 'utf8' }).status, 1);
    assert.equal(spawnSync('node', [script, 'bogus'], { encoding: 'utf8' }).status, 2);
  } finally {
    done(root);
  }
});
