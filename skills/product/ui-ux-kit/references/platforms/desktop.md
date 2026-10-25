# Desktop apps

For macOS, Windows and Linux apps, whether native, Flutter, Electron or Tauri. The user has a pointer, a keyboard and a resizable window.

## Principles

- **Every action has a keyboard path** and a visible focus state. Show the shortcut next to the command.
- **Hover, right-click and drag are shortcuts, never the only way.**
- **Density can be higher than on touch.** Controls of 32 to 36 px are normal. Keep a clear target of at least 24 px.
- **Follow the OS** for window controls, menus, file dialogs, notifications and confirm button order. Windows puts the confirm button on the left. macOS and Linux put it on the right.
- **The window resizes.** Set a minimum width. Let panes grow. Remember window size and position.
- Do not transplant phone navigation. A desktop app uses a menu bar, a toolbar, a sidebar and split views.

## Structure

| Pattern | Use |
|---|---|
| Menu bar (macOS) or app menu | Every command lives here, even if it also has a button |
| Toolbar | The frequent commands for the current view |
| Sidebar | Top-level destinations. It can collapse |
| Split view and resizable panes | List and detail. Drag to resize and remember the split |
| Context menu | Actions for the item under the pointer |
| Command palette | Many commands for expert users. It opens with a shortcut and has no animation |

## Type and targets

Body about 13 to 14 px. Smallest text 11. Targets at least 24 px with room between. Keyboard focus ring 2 px in the focus role.

## Details that make it feel native

- Scrollbars are visible on desktop. Read-only text is selectable.
- Text fields support the full keyboard: select all, word jump, undo.
- Drag and drop works where the OS expects it. Provide a menu alternative.
- Menus open on press and close on escape. Focus returns to where it was.
- Tooltips show shortcuts and appear after a short delay.
- Respect the OS accent color and appearance setting if the brand allows.
- Handle high-DPI and standard-DPI screens, and multiple displays.

## Motion

Quicker than mobile (about 0.8 times). Hover and keyboard feedback matter more than flourishes. Do not animate frequent commands or anything opened by a shortcut.

## Stack notes

Flutter desktop: adaptive layout from constraints, scrollbars on, selectable text, platform confirm order. Electron and Tauri: web rules plus the OS menu bar and native dialogs. Native macOS keeps AppKit controls and menus. Do not apply iPhone rules to it.

## Verify

Use the app with the keyboard only. Resize to the minimum width. Run on each OS you ship to. Check dark mode and the OS contrast setting.
