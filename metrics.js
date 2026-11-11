/* Live bibliographic metrics for the Publications page.
 *
 * Reads data/metrics.json (rewritten weekly by .github/workflows/update-metrics.yml)
 * and updates the stat cards. The markup already carries the last known values, so
 * with JavaScript disabled, or if the fetch fails, the page still renders the numbers
 * committed in the HTML — it simply does not refresh them.
 */

(async function () {
  const nodes = document.querySelectorAll("[data-metric]");
  if (!nodes.length) return;

  let data;
  try {
    const response = await fetch("data/metrics.json", { cache: "no-store" });
    if (!response.ok) return;
    data = await response.json();
  } catch (error) {
    return; // offline or file:// — keep the static values
  }

  const format = (value) => Number(value).toLocaleString("en-GB");

  nodes.forEach((node) => {
    const key = node.dataset.metric;
    const value = data[key];
    if (value === null || value === undefined) return;
    node.textContent = format(value);
  });

  // The "Reads" card only makes sense once a source provides that number (ADS).
  document.querySelectorAll("[data-metric-card]").forEach((card) => {
    const key = card.dataset.metricCard;
    const value = data[key];
    card.hidden = value === null || value === undefined;
  });

})();
