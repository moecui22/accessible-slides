/* The browser demo re-implements audit.py in JavaScript. If the two ever
 * disagree, the page is quietly lying to people who will never run the Python.
 *
 * This extracts the maths out of docs/index.html and checks it against the same
 * published reference values that tests/test_audit.py checks the Python against.
 *
 *     node tests/test_demo_parity.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
const js = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)]
  .map((m) => m[1])
  .join('\n');

// The page wires itself to the DOM on load. Stub enough that the pure maths
// gets defined; anything DOM-dependent may throw and is not what we are testing.
const ctx = vm.createContext({
  document: {
    getElementById: () => null,
    querySelectorAll: () => [],
    querySelector: () => null,
    addEventListener: () => {},
    createElement: () => ({ getContext: () => ({}) }),
  },
  window: { addEventListener: () => {} },
  console,
});
try {
  vm.runInContext(js, ctx);
} catch (e) {
  /* DOM wiring is expected to fail here; the maths is already defined */
}

const de = (a, b, mode) =>
  ctx.ciede2000(
    ctx.rgbLab(ctx.simulate(ctx.hexRgb(a), mode)),
    ctx.rgbLab(ctx.simulate(ctx.hexRgb(b), mode)),
  );

// Same reference values as tests/test_audit.py, to 3 decimal places.
const cases = [
  ['contrast #8a8a8a on #ffffff', ctx.contrast(ctx.hexRgb('#8a8a8a'), ctx.hexRgb('#ffffff')), 3.452],
  ['tab10 red vs green, normal', de('#d62728', '#2ca02c', 'normal'), 71.828],
  ['tab10 red vs green, deutan', de('#d62728', '#2ca02c', 'deutan'), 4.969],
  ['tab10 red vs green, protan', de('#d62728', '#2ca02c', 'protan'), 27.309],
  ['Okabe-Ito blue vs vermillion, deutan', de('#0072b2', '#d55e00', 'deutan'), 62.444],
  ['18 arcmin at 15 m on a 2 m screen (pt)', ctx.minFont(15, 2.0, 18, 0.52, 540), 40.780],
  ['24 pt at 15 m on a 2 m screen (arcmin)', ctx.arcminOf(24, 15, 2.0, 0.52, 540), 10.593],
];

let failed = 0;
for (const [name, got, want] of cases) {
  const ok = Number.isFinite(got) && Math.abs(got - want) < 0.005;
  if (!ok) failed++;
  console.log(
    `${ok ? 'PASS' : 'FAIL'} ${name.padEnd(40)} got ${Number(got).toFixed(3).padStart(8)}  want ${want.toFixed(3).padStart(8)}`,
  );
}

if (failed) {
  console.error(`\n${failed} check(s) failed: docs/index.html has drifted from scripts/audit.py.`);
  process.exit(1);
}
console.log('\nBrowser demo matches the Python.');
