# bencjhuang.github.io

Academic research group website for the **CJHuang Group** (Prof. Chen-Jui "Ben" Huang).
GitHub Pages static site — pure HTML/CSS/JS, no build step.
Prof. Huang is **Assistant Professor** in the Department of Chemical Engineering at
Taiwan Tech (NTUST); the group started in **August 2026**. Use present-tense wording
site-wide (no "incoming" / "starting August 2026").

## Editing Workflow

No build process. Edit files directly, then push:
- Changes go live automatically via GitHub Pages
- Test locally by opening HTML files in a browser (or `python3 -m http.server` from the repo root)
- Images go in `image/`; originals/backups in `image/_originals/` (git-ignored: new backups stay local)
- Web images: JPEG quality ~85, long edge ≤ 2400px
- Cache-bust changed images with a `?v=N` query string on the `src`

## Site Structure

| File | Purpose |
|------|---------|
| `index.html` | Homepage: hero (+ recruiting line), mission + 4 research cards, XCT before/after compare, stats band, news (latest 4, older behind a button), group photo + join CTA |
| `research.html` | 4 research areas: ASSBs, anode-free Li metal, operando/in-situ, X-ray tomography (µXCT) |
| `people.html` | Tabbed: PI profile (bio, education, experience, honors), Members, Alumni |
| `publications.html` | ~65 publications with impact factors, filter chips, citation stats |
| `equipment.html` | Lab + facility instruments with photos and specs |
| `gallery.html` | Filterable photo gallery with lightbox |
| `join.html` | Recruitment: postdoc, PhD, undergrad positions |
| `lab.html` | Interactive 3D lab tour (Three.js r128 + OrbitControls via CDN). Chinese-only (`lang="zh-Hant"`), linked from the nav on every page |
| `card/index.html` | Standalone digital business card (self-contained; embedded QR + vCard) |
| `zh/index.html`, `zh/research.html`, `zh/people.html`, `zh/join.html` | Traditional Chinese versions (share `../styles.css` / `../script.js`; Publications, Equipment, Gallery link to the English pages) |
| `styles.css` | All styling — CSS custom properties (design tokens) in `:root` |
| `script.js` | Sticky nav, hamburger, news filter, publications filter, people tabs, lightbox, reveal-on-scroll |
| `sitemap.xml`, `robots.txt` | SEO; `google*.html` is the Search Console verification file — do not delete |

## Design Tokens (styles.css `:root`)

Never hardcode colors or fonts inline — use these variables. Single-accent system.

| Variable | Value | Use |
|---|---|---|
| `--ink` | `#0B1220` | Near-black navy — primary text |
| `--ink-soft` | `#1f2a3d` | Secondary text |
| `--paper` | `#FAFAF7` | Warm off-white page background |
| `--surface` | `#FFFFFF` | Cards, elevated surfaces |
| `--rule` | `#E5E7EB` | Hairline borders |
| `--muted` | `#636A76` | Tertiary text (≥4.5:1 on paper) |
| `--accent` | `#C2410C` | Terracotta — the single accent (links, highlights) |
| `--accent-2` | `#9A330A` | Deeper terracotta — hover |
| `--accent-on-dark` | `#EE7D46` | Terracotta for text on `--ink` backgrounds (AA contrast) |
| `--font-display` | Fraunces (serif) | H1–H3 |
| `--font-body` | IBM Plex Sans | Body (same family as the business card) |
| `--font-mono` | JetBrains Mono | Eyebrows, tags, code-style text |

Motion uses `--ease: cubic-bezier(0.22,1,0.36,1)` with `--t-fast/med/slow`; respect
`prefers-reduced-motion`. Legacy `--color-*` aliases exist but map onto the tokens above.

## Structured Data / SEO

`index.html` and `people.html` carry JSON-LD (`Person` / `ResearchOrganization` / `WebSite`)
with `sameAs` linking Scholar, ORCID, LinkedIn, ResearchGate, and the NTUST faculty page,
plus `award` and `knowsAbout`. When PI facts change (title, awards, research areas),
update the visible HTML **and** the matching JSON-LD on both pages, then re-validate the JSON.

## Patterns & Conventions

- **BEM-like class naming**: `.member-card`, `.research-section`, `.publication`, `.project-card`, etc.
- **Filtering**: `data-filter` / `data-category` attributes; JS in `script.js` handles it
- **Tabs**: `data-tab` on people page for PI / Members / Alumni
- **Stable publication numbering**: JS assigns `data-num` (CSS counters break when items are filtered)
- **Mobile breakpoint**: 768px (hamburger menu)
- **Navigation**: hardcoded in every HTML file — update all pages when adding a nav item
- **Bilingual pages**: `index`, `research`, `people`, `join` each have a `zh/` twin. When you change
  content on one, update the other (news, stats band, positions, PI facts). Each pair is linked by
  `hreflang` tags in `<head>` and the `.nav-lang` / `.mobile-lang` switch in the nav; zh pages use
  `../` paths and load Noto Sans/Serif TC. Chinese copy uses 臺 (國立臺灣科技大學) and ROC 學年度.

## Common Editing Tasks

**Add a group member** (`people.html`, Members tab):
- Copy an existing `.member-card` block; update name, tag, bio, and photo `src`
- Photos are 3:4 portrait — crop from the original, keep a backup in `image/_originals/`

**Add a publication** (`publications.html`):
- Find the correct `.year-group`, copy an existing `.publication` entry, update all fields
- Update the citation stats block (h-index, citations) and the "last checked" date
- Also update the homepage "at a glance" band (`#numbers` in `index.html` **and** `zh/index.html`) — same numbers, plus the "as of" date in `.numbers-source` below it

**Update PI facts** (title, honors, research interests, stats):
- Edit the visible HTML **and** the JSON-LD on `index.html` + `people.html`

**Change colors or fonts**:
- Edit the design tokens in `styles.css :root` — affects the entire site

## Notes

- **Always ask before `git commit`** — never commit without explicit approval for that commit
- **Never run `git push`** — the user pushes themselves
- Never delete `google*.html` (Search Console verification file)
- Google Fonts via CDN (Fraunces, IBM Plex Sans, JetBrains Mono; the card page also loads Noto Sans/Serif TC + IBM Plex Sans)
- The `card/` page is intentionally self-contained (its own inline styles, not the main design system)

## PI Reference Facts (authoritative)

Use these exact values when editing site/CV/faculty content.

- **Name:** Chen-Jui (Ben) Huang / 黃貞睿, Ph.D. (publishing byline: C.-J. Huang)
- **Title:** Assistant Professor, Dept. of Chemical Engineering, Taiwan Tech (NTUST) — started Aug 2026
- **Email:** cjhuang@mail.ntust.edu.tw · **Office** E2-808 · **Lab** E2-301
- **Phones:** office 02-2737-6618 · lab 02-2733-3141 ext. 7603 · fax 02-2737-6644
- **ORCID:** 0000-0001-8338-1424 · **Google Scholar id:** fFTtGFAAAAAJ
- **NTUST faculty page:** https://www.ch.ntust.edu.tw/departmentmembers-76.html

**Awards (6 as of 2026-07):** Yushan Young Fellow (MOE, 2026–2031, most important) ·
CTCI Foundation Science & Technology Scholarship (2021) · Phi Tau Phi Honorary Membership (2021) ·
Ph.D. Candidate Scholarship (NSRRC, 2019/2020) · HERCULES Program (MOST/NSTC, 2019) ·
Global Networking Talent 3.0 (MOE, 2016, Hongjie Dai Lab @ Stanford).

**Citation stats change** — as of 2026-07: h-index 44 / 5,644 citations / 65 papers.
Re-check the Scholar page when updating; don't reuse old numbers.

## Ongoing: Google Authority / Knowledge Panel

Goal: make the PI/group entity clear enough for Google to auto-generate a Knowledge Panel
(can't be created manually, only claimed).

**Done (2026-07):** JSON-LD on `index.html` + `people.html`; `sameAs` to 5 sources; footer
`rel="me"` links on all main pages; `sitemap.xml` + `robots.txt`; Search Console verified;
all external profiles (Scholar, ORCID, LinkedIn, ResearchGate, NTUST) link back to the site;
Scholar affiliation verified with mail.ntust.edu.tw.

**On hold / to watch:** Wikidata entry deferred (decided 2026-07) until third-party sources
exist — e.g. NTUST onboarding press release, MOE Yushan Young Fellow announcement, media
coverage of papers.
