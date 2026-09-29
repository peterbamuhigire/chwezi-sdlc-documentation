// render.mjs — batch Mermaid renderer used by scripts/render_diagrams.py.
//
// Reads a job file (JSON) and renders every job to SVG and PNG in ONE local
// browser session, using the machine's Chrome or Edge through
// PUPPETEER_EXECUTABLE_PATH. No hosted renderer is contacted and no browser
// is downloaded. Client diagram source never leaves the machine.
//
// Job file shape:
//   { "fontCss": "<abs path to @font-face css>", "mermaidConfig": {...},
//     "bodyMeasureIn": 6.25, "maxHeightIn": 8.0, "minPpi": 300,
//     "jobs": [ { "id": "doc-1", "definition": "...", "svg": "<abs>", "png": "<abs>",
//                 "mermaidConfig": {...} (optional; replaces the shared one) } ] }
// Writes a result file next to the job file: <job>.result.json
// Exit code: 0 all rendered; 1 one or more jobs failed (details in result).

import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import puppeteer from "puppeteer";
import { renderMermaid } from "@mermaid-js/mermaid-cli";

const jobFile = process.argv[2];
if (!jobFile) {
  console.error("usage: node render.mjs <job.json>");
  process.exit(2);
}
const spec = JSON.parse(fs.readFileSync(jobFile, "utf-8"));
const executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
if (!executablePath || !fs.existsSync(executablePath)) {
  console.error(
    "PUPPETEER_EXECUTABLE_PATH must point to a local Chrome or Edge binary",
  );
  process.exit(2);
}

const customFontCSS = spec.fontCss
  ? [{ cssUrl: url.pathToFileURL(spec.fontCss), allowParentDirectoryLevel: 0 }]
  : [];

function svgSize(svgText) {
  const vb = svgText.match(/viewBox="([-\d.]+)[ ,]+([-\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)"/);
  if (vb) return { w: parseFloat(vb[3]), h: parseFloat(vb[4]) };
  return { w: 800, h: 600 };
}

const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  // Offline by construction: every request the renderer does not serve from
  // local files is sent to a dead proxy and fails, so diagram source cannot
  // leave the machine even if a diagram references a remote asset.
  args: [
    "--no-first-run",
    "--disable-extensions",
    "--disable-gpu",
    "--proxy-server=http://127.0.0.1:9",
    "--proxy-bypass-list=<-loopback>",
  ],
});
const results = [];
let failed = 0;
let fontProbe = null;
try {
  // Probe: does headless Chrome resolve the approved face from the CSS?
  if (spec.fontCss && spec.fontFamily) {
    const page = await browser.newPage();
    await page.setContent(
      `<style>${fs.readFileSync(spec.fontCss, "utf-8")}</style><p style="font-family:'${spec.fontFamily}'">Ag</p>`,
    );
    fontProbe = await page.evaluate(async (family) => {
      const loaded = await document.fonts.load(`16px "${family}"`);
      return { family, facesLoaded: loaded.length, resolved: document.fonts.check(`16px "${family}"`) && loaded.length > 0 };
    }, spec.fontFamily);
    await page.close();
    if (!fontProbe.resolved) {
      throw new Error(`font probe failed: ${spec.fontFamily} did not load`);
    }
  }
  for (const job of spec.jobs) {
    const common = {
      backgroundColor: "white",
      // A job may carry its own config (render_diagrams.py sends one for
      // Gantt charts: fixed width, label sizes, token colours, axis CSS).
      mermaidConfig: job.mermaidConfig || spec.mermaidConfig || {},
      customFontCSS,
      // The face is embedded by render_diagrams.py itself (the renderer's
      // embedder does not handle data: URI faces).
      fontEmbed: false,
    };
    try {
      const svgOut = await renderMermaid(browser, job.definition, "svg", {
        ...common,
        viewport: { width: 4000, height: 3000, deviceScaleFactor: 1 },
      });
      const svgText = new TextDecoder().decode(svgOut.data);
      const { w, h } = svgSize(svgText);
      // Printed width: the body measure, reduced when the figure would be too tall.
      let printedWidthIn = spec.bodyMeasureIn;
      if ((h / w) * printedWidthIn > spec.maxHeightIn) {
        printedWidthIn = (spec.maxHeightIn * w) / h;
      }
      const scale = Math.min(
        12,
        Math.max(2, Math.ceil((spec.minPpi * printedWidthIn) / w)),
      );
      const pngOut = await renderMermaid(browser, job.definition, "png", {
        ...common,
        viewport: {
          width: Math.ceil(w) + 64,
          height: Math.ceil(h) + 64,
          deviceScaleFactor: scale,
        },
      });
      fs.mkdirSync(path.dirname(job.svg), { recursive: true });
      fs.writeFileSync(job.svg, svgOut.data);
      fs.writeFileSync(job.png, pngOut.data);
      const png = Buffer.from(pngOut.data);
      const pxW = png.readUInt32BE(16);
      const pxH = png.readUInt32BE(20);
      results.push({
        id: job.id,
        ok: true,
        svgWidth: w,
        svgHeight: h,
        scale,
        pngWidthPx: pxW,
        pngHeightPx: pxH,
        printedWidthIn,
        ppi: Math.floor(pxW / printedWidthIn),
      });
    } catch (err) {
      failed += 1;
      results.push({ id: job.id, ok: false, error: String(err?.message || err) });
    }
  }
} finally {
  await browser.close();
}
fs.writeFileSync(
  jobFile.replace(/\.json$/, "") + ".result.json",
  JSON.stringify({ fontProbe, results }, null, 2),
);
process.exit(failed ? 1 : 0);
