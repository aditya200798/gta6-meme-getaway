// Entry program for make.fun bounty gta6-meme-x-01 ("Post a GTA 6 meme on X").
//
// The entry itself is the X post: my agent made the meme (see meme.png and
// build_meme.py), it was posted on X from a public account with the bounty
// link, the @makefunai tag and the play code in its text, and POST.json in
// this repository names that post. The house reads the post from X and the
// judge sees its first picture and its text; nothing this program writes
// about the post is judged.
//
// All this program has to do is hand POST.json to the grader: copy it from
// the repository root (MAKEFUN_BOT_DIR, /bot in the grader) into the output
// directory (MAKEFUN_OUTPUT_DIR, /output in the grader), byte for byte.
// Before copying, it sanity-checks that POST.json parses as a JSON object
// with a string "url", so a broken file fails loudly here instead of
// silently at the gate. No network, no clock, no files outside the repo.
//
// Local run, exactly the way the grader runs it:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const postPath = join(botDir, 'POST.json');

let parsed: unknown;
try {
  parsed = JSON.parse(readFileSync(postPath, 'utf8'));
} catch (err) {
  console.error(`POST.json is not readable JSON in ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}

if (
  typeof parsed !== 'object' ||
  parsed === null ||
  typeof (parsed as { url?: unknown }).url !== 'string'
) {
  console.error('POST.json must be a JSON object like {"url": "https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(postPath, join(outputDir, 'POST.json'));
