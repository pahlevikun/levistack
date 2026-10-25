/*
 * Run this in the page (DevTools console, or a browser-automation "run JavaScript" tool).
 * It reads computed styles from the elements actually on screen and prints one JSON string.
 * Save the JSON to a file, then:  extract_site.py --browser-json file.json --out extracted.json
 *
 * It sees what the user sees: CSS-in-JS, themes set by script, and the active color scheme.
 * It reads styles only. It sends nothing anywhere.
 */
(() => {
  const MAX = 3000;
  const els = [document.documentElement, document.body].concat(Array.from(document.querySelectorAll("body *")).slice(0, MAX));
  const sizeOf = (el) => (el === document.body || el === document.documentElement) ? { width: innerWidth, height: innerHeight } : el.getBoundingClientRect();
  const bump = (o, k, n = 1) => { if (k) o[k] = (o[k] || 0) + n; };
  const hex = (c) => {
    const m = c && c.match(/rgba?\(([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)(?:[ ,/]+([\d.]+))?/);
    if (!m) return null;
    const a = m[4] === undefined ? 1 : parseFloat(m[4]);
    if (a < 0.5) return null;
    return "#" + [m[1], m[2], m[3]].map((v) => Math.round(parseFloat(v)).toString(16).padStart(2, "0")).join("").toUpperCase();
  };
  const out = { url: location.href, title: document.title, text: {}, bg: {}, border: {}, fonts: {}, sizes: {}, weights: {}, radii: {}, shadows: {}, gaps: {}, durations: [], easings: {}, faces: [], custom_props: {}, dark_media: false };
  for (const el of els) {
    const r = sizeOf(el);
    if (r.width < 2 || r.height < 2) continue;
    const s = getComputedStyle(el);
    if (s.display === "none" || s.visibility === "hidden") continue;
    const area = Math.min(r.width * r.height, 200000) / 1000 + 1;
    const hasText = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim());
    if (hasText) {
      bump(out.text, hex(s.color));
      bump(out.fonts, (s.fontFamily.split(",")[0] || "").replace(/["']/g, "").trim());
      bump(out.sizes, parseFloat(s.fontSize));
      bump(out.weights, s.fontWeight);
    }
    bump(out.bg, hex(s.backgroundColor), area);
    if (parseFloat(s.borderTopWidth) > 0) bump(out.border, hex(s.borderTopColor));
    const rad = parseFloat(s.borderTopLeftRadius);
    if (rad > 0) bump(out.radii, rad >= 100 ? 9999 : Math.round(rad));
    if (s.boxShadow && s.boxShadow !== "none") bump(out.shadows, s.boxShadow.slice(0, 120));
    for (const p of ["paddingTop", "paddingLeft", "marginTop", "rowGap", "columnGap"]) {
      const v = parseFloat(s[p]);
      if (v > 0 && v <= 160) bump(out.gaps, Math.round(v));
    }
    const td = parseFloat(s.transitionDuration);
    if (td > 0) { out.durations.push(Math.round(td * (s.transitionDuration.includes("ms") ? 1 : 1000))); bump(out.easings, s.transitionTimingFunction.split(",")[0]); }
  }
  try {
    for (const f of document.fonts) out.faces.push(f.family.replace(/["']/g, ""));
    out.faces = Array.from(new Set(out.faces));
  } catch (e) { /* fonts API missing */ }
  const root = getComputedStyle(document.documentElement);
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const rule of rules) {
      if (rule.media && /prefers-color-scheme:\s*dark/.test(rule.media.mediaText)) out.dark_media = true;
      if (rule.selectorText === ":root" && rule.style) {
        for (const name of Array.from(rule.style).filter((n) => n.startsWith("--")).slice(0, 80)) out.custom_props[name] = root.getPropertyValue(name).trim();
      }
    }
  }
  console.log(JSON.stringify(out));
  return JSON.stringify(out);
})();
