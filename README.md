# Luiz A. Silva Lima — personal website

Static personal website (plain HTML + one CSS file), published with GitHub Pages.
The visual design lives in Penpot ("Personal website" page, style guide v1.0);
this repository is the hand-written, responsive implementation of it.

## Structure

| Path | Purpose |
| --- | --- |
| `index.html` | Home: hero, profile link cards |
| `research.html` | Research overview + five research cards |
| `publications.html` | Refereed papers, preprints/proceedings, software, metrics |
| `codes.html` | Software and pipelines |
| `cv.html` | Full CV as four A4 sheets + PDF download |
| `contact.html` | Contact addresses |
| `404.html` | Not-found page |
| `style.css` | Design tokens, layout, components, responsive and print rules |
| `assets/luiz-silva-lima-cv.pdf` | CV source (LaTeX build, November 2026) |
| `assets/cv/page-*.png` | CV pages rasterised at 1166 px wide for the web |
| `images/` | Research figures, portrait, profile icons, Open Graph card |
| `robots.txt`, `sitemap.xml` | Crawler directives and indexable URLs |
| `data/metrics.js` | The stat-card numbers on the Publications page — the only copy |
| `metrics.js` | Reads those values and fills the stat cards |
| `_archive/` | Superseded pages and the old shared-footer component (gitignored) |

## Design system

Derived from the Penpot style guide, defined as custom properties at the top of `style.css`.

- **Type** — Source Sans Pro / Source Sans 3. H1 40/400/1.0, hero 48/700/1.05,
  H2 32, H3 24, subheading 20/1.2, body 16/1.5, caption 13–14/1.5,
  eyebrow 13/700 uppercase.
- **Colour** — page `#F7F8F7`, card `#FFFFFF`, header and footer `#EFEFEF`,
  ink `#0A1015`, muted `#5F6B72`, inverse `#F2F2F2`, primary `#015958`
  (hover `#014A49`, pressed `#013F3E`), border `#D8DFE1`, strong `#7E8B91`.
- **Layout** — 1366 px frame with a 100 px gutter and 1166 px content column;
  mobile 390 px frame with a 24 px gutter. Radius 6 px, spacing scale 8/16/24/32/48/100.
  No shadows, no gradients.

## Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Refreshing the CV

The CV page shows rasterised pages of `assets/luiz-silva-lima-cv.pdf`, so the page and
the download always match. After rebuilding the PDF from the LaTeX sources:

```bash
cp /path/to/curriculum_vitae.pdf assets/luiz-silva-lima-cv.pdf
rm -f assets/cv/page-*.png
pdftoppm -r 141 -png assets/luiz-silva-lima-cv.pdf assets/cv/page
```

`-r 141` produces 1166 px wide pages, matching the design frame. If the page count
changes, add or remove a `<figure class="cv-sheet">` block in `cv.html`.

## Publishing to GitHub Pages

1. Repository: `luizsl.github.io`.
2. Push `main`.
3. Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
4. The site appears at <https://luizsl.github.io/>.

## Being found on Google

On-page basics are in place: unique `<title>` and `description` on every page,
`rel="canonical"`, Open Graph and Twitter card tags with a 1200x630 preview image,
`Person` + `WebSite` structured data (JSON-LD) naming ORCID, ADS, Scholar, GitHub,
LinkedIn and Instagram as `sameAs`, plus `robots.txt` and `sitemap.xml`.

Off-page steps that actually determine ranking:

1. **Google Search Console** — add `https://luizsl.github.io/` as a URL-prefix
   property, verify ownership (HTML file upload is easiest on Pages: drop the file
   Google gives you in this folder and re-deploy), then submit `sitemap.xml`.
   Use *URL Inspection* to request indexing of the six pages.
2. **Cross-link from authoritative profiles** — add `https://luizsl.github.io/` to
   ORCID, NASA ADS, Google Scholar, GitHub and LinkedIn. Those `sameAs` links are
   what let Google merge the site with the existing "Luiz A. Silva Lima" entities.
3. Time. A new subdomain has no history; expect days to weeks for the first
   crawl, longer for a search for the bare name.

## Editing the metrics

The four stat cards on the Publications page get their numbers from
`data/metrics.js` and nowhere else. Edit the object, save, reload — no build
step, no scheduled job:

```js
window.siteMetrics = {
  publications: "12+",
  citations: "135+",
  h_index: 6,
  reads: "3570+"
};
```

- A bare number (`6`) or a quoted string (`"12+"`), it makes no difference: the
  digits are grouped with a non-breaking space, so `3570+` renders as `3 570+`.
- `reads` is the NASA ADS read count; set it to `null` to show a dash.
- It is loaded with a `<script>` tag rather than fetched as JSON, so the numbers
  also appear when the page is opened directly from disk. `fetch()` is blocked
  on `file://` origins, which would otherwise leave the cards blank.

## Known gaps

- The HST composite in the first research card exists only inside the Penpot file
  (an unnamed 392x199 bitmap) and could not be exported to disk. The "Galactic
  Rivers" card therefore shows a dashed "Figure pending" box in `research.html`;
  export that image from Penpot into `images/` and swap the block.
- The research intro has no portrait/aside image (the Penpot board has one that could
  not be exported as a file).
- Footer "Social" links point to the LinkedIn and Instagram profiles; the four brand
  marks on the profile cards are monogram tiles rather than official logos.
- Metric values are entered by hand from NASA ADS; they are only as current as
  the last commit to `data/metrics.js`.
