#!/usr/bin/env node
// HTML を A4 の PDF にする（デジタル商品用）。日本語は IPA ゴシックで表示される。
//
// 使い方:
//   node automation/tools/html2pdf.cjs 原稿.html 出力.pdf
//
// 原稿が <html> を含まない断片なら、読みやすい基本スタイルで包んでから変換する。
// 生成した PDF はリポジトリに入れない（公開リポジトリのため）。HQ のアセットにアップロードする。

const fs = require("fs");
const { chromium } = require("playwright");

const BASE_CSS = `
  @page { size: A4; }
  html { font-family: "IPAPGothic", "IPAGothic", sans-serif; font-size: 10.5pt; line-height: 1.85; color: #1b2333; }
  body { margin: 0; }
  h1 { font-size: 22pt; line-height: 1.35; margin: 0 0 12pt; padding-bottom: 8pt; border-bottom: 3px solid #233f7a; }
  h2 { font-size: 15pt; margin: 22pt 0 8pt; padding-left: 8pt; border-left: 5px solid #c2412d; page-break-after: avoid; }
  h3 { font-size: 12pt; margin: 16pt 0 6pt; page-break-after: avoid; }
  p, li { orphans: 3; widows: 3; }
  code, pre { font-family: "IPAGothic", monospace; font-size: 9pt; }
  pre { background: #f2f4f7; border: 1px solid #d8dde5; border-radius: 4pt; padding: 8pt 10pt; white-space: pre-wrap; word-break: break-all; page-break-inside: avoid; }
  table { border-collapse: collapse; width: 100%; margin: 8pt 0; page-break-inside: avoid; }
  th, td { border: 1px solid #c9d0da; padding: 4pt 6pt; text-align: left; vertical-align: top; }
  th { background: #eef1f6; }
  blockquote { margin: 8pt 0; padding: 6pt 12pt; background: #f6f7f9; border-left: 4px solid #9aa6b8; }
  .cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always; }
  .cover h1 { font-size: 28pt; border: 0; }
  .note { font-size: 9pt; color: #5b6573; }
  .pagebreak { page-break-after: always; }
`;

async function main() {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) {
    console.error("usage: node automation/tools/html2pdf.cjs input.html output.pdf");
    process.exit(1);
  }
  let html = fs.readFileSync(input, "utf8");
  if (!/<html[\s>]/i.test(html)) {
    html = `<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>${BASE_CSS}</style></head><body>${html}</body></html>`;
  }
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: "load" });
    await page.pdf({
      path: output,
      format: "A4",
      printBackground: true,
      margin: { top: "18mm", bottom: "18mm", left: "16mm", right: "16mm" },
      displayHeaderFooter: true,
      headerTemplate: "<div></div>",
      footerTemplate:
        '<div style="font-size:8px;width:100%;text-align:center;color:#8a93a3"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    });
  } finally {
    await browser.close();
  }
  console.log(`PDF: ${output}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
