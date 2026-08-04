import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import MarkdownIt from 'markdown-it'
import texmath from 'markdown-it-texmath'
import katex from 'katex'
import container from 'markdown-it-container'
import anchor from 'markdown-it-anchor'

export const CALLOUTS = {
  goal: { icon: '🎯', label: 'Goal' },
  gap: { icon: '🔗', label: 'Going deeper' },
  insight: { icon: '💡', label: 'Insight' },
  qa: { icon: '❓', label: 'Q&A' },
  warning: { icon: '⚠️', label: 'Warning' },
  summary: { icon: '📌', label: 'Takeaway' },
}

export function slugify(s) {
  return String(s).trim().toLowerCase()
    .replace(/[^\wㄱ-힝]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

export function createRenderer() {
  const md = new MarkdownIt({ html: true })
  md.use(texmath, {
    engine: katex,
    delimiters: 'dollars',
    katexOptions: { throwOnError: false },
  })
  md.use(anchor, { slugify })
  for (const [name, meta] of Object.entries(CALLOUTS)) {
    md.use(container, name, {
      render(tokens, idx) {
        const tok = tokens[idx]
        if (tok.nesting === 1) {
          const custom = tok.info.trim().slice(name.length).trim()
          const title = custom || meta.label
          return `<div class="callout callout-${name}"><p class="callout-title"><span class="callout-icon">${meta.icon}</span>${md.utils.escapeHtml(title)}</p>\n`
        }
        return '</div>\n'
      },
    })
  }
  return md
}

const MIME = {
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.svg': 'image/svg+xml',
}

export function extractToc(md, src) {
  const tokens = md.parse(src, {})
  const toc = []
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i]
    if (t.type === 'heading_open' && (t.tag === 'h2' || t.tag === 'h3')) {
      const text = tokens[i + 1].children
        .filter(c => ['text', 'code_inline', 'math_inline'].includes(c.type))
        .map(c => c.content).join('')
      toc.push({ level: Number(t.tag[1]), text, id: slugify(text) })
    }
  }
  return toc
}

export function renderToc(toc) {
  if (!toc.length) return ''
  const items = toc
    .map(h => `<li class="toc-l${h.level}"><a href="#${h.id}">${h.text}</a></li>`)
    .join('\n')
  return `<nav class="toc"><p class="toc-label">Contents</p><ul>\n${items}\n</ul></nav>\n`
}

export function inlineImages(html, baseDir) {
  return html.replace(/(<img[^>]*\ssrc=")([^"]+)(")/g, (m, pre, src, post) => {
    if (/^(data:|https?:)/.test(src)) return m
    const p = path.resolve(baseDir, decodeURI(src))
    if (!fs.existsSync(p)) {
      console.warn(`warning: missing image ${src}`)
      return m
    }
    const mime = MIME[path.extname(p).toLowerCase()] || 'application/octet-stream'
    return `${pre}data:${mime};base64,${fs.readFileSync(p).toString('base64')}${post}`
  })
}

export function rewriteMdLinks(html) {
  return html.replace(/(<a[^>]*\shref=")([^"#]+)\.md(#[^"]*)?(")/g,
    (m, pre, base, hash, post) =>
      /^https?:/.test(base) ? m : `${pre}${base}.html${hash || ''}${post}`)
}

export function katexCss() {
  const require = createRequire(import.meta.url)
  const cssPath = require.resolve('katex/dist/katex.min.css')
  const dist = path.dirname(cssPath)
  let css = fs.readFileSync(cssPath, 'utf8')
  css = css.replace(
    /src:url\(fonts\/([^)]+)\.woff2\) format\("woff2"\)[^;}]*/g,
    (m, name) => {
      const buf = fs.readFileSync(path.join(dist, 'fonts', `${name}.woff2`))
      return `src:url(data:font/woff2;base64,${buf.toString('base64')}) format("woff2")`
    })
  return css
}

export function page({ title, tocHtml, bodyHtml, css }) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<style>
${css}
</style>
</head>
<body>
<main class="note">
${tocHtml}${bodyHtml}</main>
</body>
</html>
`
}

function main() {
  const args = process.argv.slice(2)
  const oIdx = args.indexOf('-o')
  const out = oIdx >= 0 ? args[oIdx + 1] : null
  const input = args.find(a => a.endsWith('.md'))
  if (!input) {
    console.error('usage: render.mjs <input.md> [-o out.html]')
    process.exit(1)
  }
  const src = fs.readFileSync(input, 'utf8')
  const md = createRenderer()
  let body = md.render(src)
  body = inlineImages(body, path.dirname(input))
  body = rewriteMdLinks(body)
  const title = (src.match(/^#\s+(.+)$/m) || [null, path.basename(input, '.md')])[1]
  const skillCss = fs.readFileSync(new URL('../assets/style.css', import.meta.url), 'utf8')
  const toc = renderToc(extractToc(md, src))
  if (toc) {
    body = body.includes('</h1>') ? body.replace('</h1>', `</h1>\n${toc}`) : toc + body
  }
  const html = page({
    title,
    tocHtml: '',
    bodyHtml: body,
    css: `${katexCss()}\n${skillCss}`,
  })
  const dest = out || path.join(path.dirname(input), 'build', `${path.basename(input, '.md')}.html`)
  fs.mkdirSync(path.dirname(dest), { recursive: true })
  fs.writeFileSync(dest, html)
  console.log(dest)
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
