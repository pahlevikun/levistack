// Minimal frontmatter parser: top-level `key: value` lines, plus `>` / `|` block scalars.
// `unsafe` lists keys whose plain (unquoted) value strict YAML parsers reject.
export function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return { data: {}, body: text, hasFrontmatter: false, unsafe: [] };
  const data = {};
  const unsafe = [];
  const lines = m[1].split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    let v = kv[2].trim();
    const block = v.match(/^([>|])[+-]?$/);
    if (block) {
      const parts = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || lines[i + 1].trim() === '')) {
        parts.push(lines[++i].trim());
      }
      v = block[1] === '>' ? parts.join(' ').replace(/\s+/g, ' ').trim() : parts.join('\n').trim();
    } else if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    } else if (/:\s|\s#|^[&*!%@`'"]/.test(v)) {
      unsafe.push(kv[1]);
    }
    data[kv[1]] = v;
  }
  return { data, body: m[2], hasFrontmatter: true, unsafe };
}
