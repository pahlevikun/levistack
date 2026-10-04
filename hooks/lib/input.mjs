// Normalize hook stdin from Claude Code (`tool_input.*`) and Cursor (top-level `command`, `file_path`).
export function normalize(raw) {
  const r = raw && typeof raw === 'object' ? raw : {};
  const t = r.tool_input && typeof r.tool_input === 'object' ? r.tool_input : {};
  return {
    raw: r,
    event: r.hook_event_name ?? '',
    tool: r.tool_name ?? '',
    command: String(t.command ?? r.command ?? ''),
    filePath: String(t.file_path ?? t.path ?? r.file_path ?? r.path ?? r.filePath ?? ''),
    offset: t.offset ?? r.offset,
    limit: t.limit ?? r.limit,
    cwd: r.cwd ?? r.workspace_roots?.[0] ?? process.cwd(),
  };
}
