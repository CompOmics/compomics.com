// Quarto pre-render guard for the team page.
//
// The team cards are wired up by one big inline <script> in team/index.qmd that
// starts with `const memberData = { ... }`. A single JS syntax error there (a
// missing comma, a stray character) aborts the ENTIRE script, so every card
// stops responding to clicks — and nothing warns you. This check runs before
// each render and fails the build loudly when that would happen.
//
// It verifies two things:
//   1. memberData parses as valid JavaScript.
//   2. Every `data-member="x"` card has a matching entry in memberData
//      (and each entry has a title), so no card is silently dead.
//
// Runs on Quarto's bundled Deno — no extra dependency. Run manually with:
//   quarto run scripts/check-team-data.js

const FILE = Deno.args[0] || "team/index.qmd";

function fail(msg) {
  console.error("\n\x1b[31m[check-team-data] BUILD BLOCKED\x1b[0m");
  console.error(msg + "\n");
  Deno.exit(1);
}

let src;
try {
  src = Deno.readTextFileSync(FILE);
} catch (e) {
  fail(`Cannot read ${FILE}: ${e.message}`);
}

// ── 1. Extract the memberData object literal (string-aware brace matching) ────
const marker = "const memberData";
const mi = src.indexOf(marker);
if (mi === -1) fail(`\`${marker}\` not found in ${FILE}. Did the script move or get renamed?`);

const start = src.indexOf("{", mi);
let depth = 0, inStr = null, esc = false, end = -1;
for (let i = start; i < src.length; i++) {
  const c = src[i];
  if (inStr) {
    if (esc) esc = false;
    else if (c === "\\") esc = true;
    else if (c === inStr) inStr = null;
    continue;
  }
  if (c === "'" || c === '"' || c === "`") { inStr = c; continue; }
  if (c === "{") depth++;
  else if (c === "}") { depth--; if (depth === 0) { end = i; break; } }
}
if (end === -1) fail("Could not find the end of the memberData object (unbalanced braces?).");

const objText = src.slice(start, end + 1);

// ── 2. Syntax-validate by evaluating just the object literal ──────────────────
let data;
try {
  data = (0, eval)("(" + objText + ")");
} catch (e) {
  fail(
    `memberData has a JavaScript error, which would kill the whole team script\n` +
    `and stop every card from opening:\n\n    ${e.message}\n\n` +
    `Fix the object literal in ${FILE} (most often a missing comma between entries).`,
  );
}

const keys = new Set(Object.keys(data));

// ── 3. Every card must map to a data entry, and every entry needs a title ─────
const members = [...src.matchAll(/data-member="([^"]+)"/g)].map((m) => m[1]);
const missing = [...new Set(members.filter((m) => !keys.has(m)))];
if (missing.length) {
  fail(
    `These team cards have no matching memberData entry, so clicking them does nothing:\n` +
    missing.map((m) => `    - data-member="${m}"`).join("\n"),
  );
}

const titleless = [...keys].filter((k) => members.includes(k) && !data[k].title);
if (titleless.length) {
  fail(`These memberData entries are missing a \`title\`:\n` + titleless.map((k) => `    - ${k}`).join("\n"));
}

// ── 4. Orphan entries (data but no card) are harmless — just note them ────────
const used = new Set(members);
const orphans = [...keys].filter((k) => !used.has(k));
if (orphans.length) {
  console.warn(`[check-team-data] note: memberData entries with no card (harmless): ${orphans.join(", ")}`);
}

console.log(`[check-team-data] OK — ${keys.size} members, ${members.length} cards, all matched.`);
