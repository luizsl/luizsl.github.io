/* Stat cards for the Publications page.
 *
 * Reads window.siteMetrics, defined in data/metrics.js — the single place the
 * numbers live — and fills the cards. Loading that file with a <script> tag
 * rather than fetch() means the numbers also appear when the page is opened
 * straight from disk, where file:// blocks XHR.
 */

(function () {
  const nodes = document.querySelectorAll("[data-metric]");
  if (!nodes.length) return;

  const data = window.siteMetrics;
  if (!data) {
    console.warn("data/metrics.js did not load; keeping the placeholder dashes");
    return;
  }

  // Thousands separated by a non-breaking space (3 570), never a comma, and
  // never wrapped across two lines.
  const group = (digits) => digits.replace(/\B(?=(\d{3})+(?!\d))/g, "\u00A0");

  const render = (value) => {
    if (typeof value === "number") return group(String(value));

    const text = String(value).trim();
    const match = text.match(/^(\d+)(\D*)$/);
    if (match) return group(match[1]) + match[2];

    return text;
  };

  nodes.forEach((node) => {
    const value = data[node.dataset.metric];
    if (value === null || value === undefined) return;
    node.textContent = render(value);
  });
})();
