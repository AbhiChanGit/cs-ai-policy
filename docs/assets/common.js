// Shared helpers for all pages: nav, tooltip, bar lists, tables. No libraries.
const PAGES = [
  ["index.html", "Findings"],
  ["tests.html", "Validation"],
  ["timeline.html", "Timeline"],
  ["tokens.html", "Tokens"],
];

function nav(current) {
  const h = document.createElement("header");
  h.className = "top";
  h.innerHTML = `<div class="in"><span class="brand">CS departments &amp; genAI</span><nav>${
    PAGES.map(([href, name]) => `<a href="${href}" class="${href === current ? "on" : ""}">${name}</a>`).join("")
  }</nav></div>`;
  document.body.prepend(h);
}

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const nice = (s) => String(s).replace(/_/g, " ");
const fmt = (n) => Number(n).toLocaleString("en-US");

const tip = (() => {
  const el = document.createElement("div");
  el.className = "tip";
  document.addEventListener("DOMContentLoaded", () => document.body.appendChild(el));
  return {
    show(html, e) { el.innerHTML = html; el.style.display = "block"; this.move(e); },
    move(e) { el.style.left = Math.min(e.clientX + 14, innerWidth - 290) + "px"; el.style.top = e.clientY + 14 + "px"; },
    hide() { el.style.display = "none"; },
  };
})();

function hoverable(node, html) {
  node.addEventListener("mouseenter", (e) => tip.show(html, e));
  node.addEventListener("mousemove", (e) => tip.move(e));
  node.addEventListener("mouseleave", () => tip.hide());
}

// Horizontal bar list. items: [{label, n, hint?}]; total used for % in tooltip.
function barList(el, items, total, color) {
  const max = Math.max(1, ...items.map((d) => d.n));
  el.classList.add("bars");
  el.innerHTML = "";
  for (const d of items) {
    const row = document.createElement("div");
    row.className = "bar";
    row.innerHTML = `<span class="lab">${esc(nice(d.label))}</span><span class="track"><span class="fill" style="width:${(d.n / max) * 100}%;${color ? `background:${color}` : ""}"></span></span><span class="num">${d.n}</span>`;
    const pct = total ? ` (${Math.round((d.n / total) * 100)}%)` : "";
    hoverable(row, `<b>${esc(nice(d.label))}</b>: ${d.n}${pct}${d.hint ? "<br>" + esc(d.hint) : ""}`);
    el.appendChild(row);
  }
}

// Sortable table. cols: [{key, label, render?}]
function table(el, cols, rows) {
  let sortKey = null, dir = 1;
  function draw() {
    const data = sortKey ? [...rows].sort((a, b) => (a[sortKey] > b[sortKey] ? dir : a[sortKey] < b[sortKey] ? -dir : 0)) : rows;
    el.innerHTML = `<table><thead><tr>${cols.map((c) => `<th data-k="${c.key}">${esc(c.label)}${sortKey === c.key ? (dir > 0 ? " ▲" : " ▼") : ""}</th>`).join("")}</tr></thead><tbody>${
      data.map((r) => `<tr>${cols.map((c) => `<td>${c.render ? c.render(r) : esc(r[c.key])}</td>`).join("")}</tr>`).join("")
    }</tbody></table>`;
    el.querySelectorAll("th").forEach((th) => th.addEventListener("click", () => {
      const k = th.dataset.k; dir = sortKey === k ? -dir : 1; sortKey = k; draw();
    }));
  }
  draw();
}

// Tiny markdown for REVIEW.md: headings, bullets, bold, code, paragraphs.
function miniMd(md) {
  return md.split(/\n{2,}/).map((block) => {
    const inline = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`(.+?)`/g, "<code>$1</code>");
    if (/^#{1,3} /.test(block)) return `<h3>${inline(block.replace(/^#+ /, ""))}</h3>`;
    if (/^- /m.test(block)) return `<ul>${block.split("\n").filter((l) => l.startsWith("- ")).map((l) => `<li>${inline(l.slice(2))}</li>`).join("")}</ul>`;
    return `<p>${inline(block)}</p>`;
  }).join("");
}
