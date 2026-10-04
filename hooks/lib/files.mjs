import { closeSync, openSync, readSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, resolve } from 'node:path';

export const levistackHome = () => process.env.LEVISTACK_HOME || join(homedir(), '.levistack');

export function isFile(path) {
  try {
    return statSync(path).isFile();
  } catch {
    return false;
  }
}

export const resolveFrom = (cwd, path) => resolve(cwd, path);

// Same count as `wc -l`: number of newline bytes.
export function countLines(path) {
  const fd = openSync(path, 'r');
  try {
    const buf = Buffer.alloc(64 * 1024);
    let lines = 0;
    for (let n = readSync(fd, buf, 0, buf.length, null); n > 0; n = readSync(fd, buf, 0, buf.length, null)) {
      for (let i = 0; i < n; i++) if (buf[i] === 10) lines++;
    }
    return lines;
  } finally {
    closeSync(fd);
  }
}

// First `bytes` of a file as text; '' when unreadable.
export function readHead(path, bytes = 2048) {
  try {
    const fd = openSync(path, 'r');
    try {
      const buf = Buffer.alloc(bytes);
      return buf.toString('utf8', 0, readSync(fd, buf, 0, bytes, 0));
    } finally {
      closeSync(fd);
    }
  } catch {
    return '';
  }
}
