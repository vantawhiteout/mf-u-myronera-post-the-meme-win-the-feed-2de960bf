// make.fun "Post the Meme, Win the Feed" entry.
//
// The entry is the X post itself. This program's only job is the one the rules
// give it: copy POST.json from the repository root to /output/POST.json, where
// the house's gate reads it. It does no network access, reads no files outside
// the repository, and writes the same bytes on every run.
//
// Outside the grader's container the two environment variables below stand in
// for /bot and /output so the exact code path can be exercised locally:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const BOT_DIR = resolve(process.env.MAKEFUN_BOT_DIR ?? '/bot');
const OUTPUT_DIR = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');

const source = join(BOT_DIR, 'POST.json');
const destination = join(OUTPUT_DIR, 'POST.json');

interface PostFile {
  url: string;
}

/** Read POST.json and fail loudly if it cannot name a post for the gate. */
function readPostFile(path: string): PostFile {
  let parsed: unknown;
  try {
    parsed = JSON.parse(readFileSync(path, 'utf8'));
  } catch (err) {
    console.error(`POST.json is not readable JSON: ${(err as Error).message}`);
    process.exit(1);
  }
  if (
    typeof parsed !== 'object' ||
    parsed === null ||
    typeof (parsed as { url?: unknown }).url !== 'string'
  ) {
    console.error('POST.json must be an object with a string "url" field.');
    process.exit(1);
  }
  return parsed as PostFile;
}

// The house owns the checks on the post address itself (shape, window, media,
// mention, play code). This program only guarantees it hands a well-formed
// JSON object to /output, so the two runs always write identical bytes.
readPostFile(source);
mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(source, destination);
