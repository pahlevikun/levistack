// Desktop notification when the agent finishes (macOS), terminal bell elsewhere.
import { execFileSync } from 'node:child_process';
import { allow } from './lib/result.mjs';

export const meta = {
  event: 'Stop',
  description: 'Desktop notification when the agent finishes (terminal bell off macOS)',
};

export default function notifyDone() {
  try {
    if (process.platform === 'darwin') {
      execFileSync('osascript', ['-e', 'display notification "Agent finished" with title "levistack"'], { stdio: 'ignore' });
    } else {
      process.stderr.write('\x07');
    }
  } catch {
    // notification is best-effort
  }
  return allow();
}
