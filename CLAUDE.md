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
- Images go in `image/`; originals/backups in `image/_originals/`
- Cache-bust changed images with a `?v=N` query string on the `src`

## Site Structure

| File | Purpose |
|------|---------|
| `index.html` | Homepage: full-bleed hero, mission, filterable news timeline, research preview |
| `research.html` | 4 research areas: ASSBs, anode-free Li metal, operando/in-situ, X-ray tomography (µXCT) |
| `people.html` | Tabbed: PI profile (bio, education, experience, honors), Members, Alumni |
| `publications.html` | ~65 publications with impact factors, filter chips, citation stats |
| `equipment.html` | Lab + facility instruments with photos and specs |
| `gallery.html` | Filterable photo gallery with lightbox |
| `join.html` | Recruitment: postdoc, PhD, undergrad positions |
| `card/index.html` | Standalone digital business card (self-contained; embedded QR + vCard) |
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
| `--muted` | `#6B7280` | Tertiary text |
| `--accent` | `#C2410C` | Terracotta — the single accent (links, highlights) |
| `--accent-2` | `#9A330A` | Deeper terracotta — hover |
| `--font-display` | Fraunces (serif) | H1–H3 |
| `--font-body` | Inter | Body |
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

## Common Editing Tasks

**Add a group member** (`people.html`, Members tab):
- Copy an existing `.member-card` block; update name, tag, bio, and photo `src`
- Photos are 3:4 portrait — crop from the original, keep a backup in `image/_originals/`

**Add a publication** (`publications.html`):
- Find the correct `.year-group`, copy an existing `.publication` entry, update all fields
- Update the citation stats block (h-index, citations) and the "last checked" date

**Update PI facts** (title, honors, research interests, stats):
- Edit the visible HTML **and** the JSON-LD on `index.html` + `people.html`

**Change colors or fonts**:
- Edit the design tokens in `styles.css :root` — affects the entire site

## Notes

- **Never run `git commit` or `git push`** — always ask first; the user handles all commits and pushes
- Google Fonts via CDN (Fraunces, Inter, JetBrains Mono; the card page also loads Noto Sans/Serif TC + IBM Plex Sans)
- The `card/` page is intentionally self-contained (its own inline styles, not the main design system)
