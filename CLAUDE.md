# bencjhuang.github.io

Academic research group website for the **CJHuang Group** (Prof. Chen-Jui "Ben" Huang).
GitHub Pages static site — pure HTML/CSS/JS, no build step.
Group joining Taiwan Tech (NTUST) as Incoming Assistant Professor in August 2026.

## Editing Workflow

No build process. Edit files directly, then push:
- Changes go live automatically via GitHub Pages
- Test locally by opening HTML files in a browser
- Images go in `image/`; use `placeholder.jpg` as fallback

## Site Structure

| File | Purpose |
|------|---------|
| `index.html` | Homepage: hero carousel, mission, filterable news |
| `research.html` | 3 research areas: ASSBs, operando/in-situ, X-ray tomography |
| `people.html` | Tabbed: PI profile, current members, alumni |
| `publications.html` | 63+ publications with impact factors and citation stats |
| `equipment.html` | Lab instruments with photos and specs |
| `gallery.html` | Filterable photo gallery |
| `join.html` | Recruitment: postdoc, PhD, undergrad positions |
| `styles.css` | All styling — 1835 lines, CSS custom properties |
| `script.js` | Hero carousel, sticky nav, hamburger menu, news filter, back-to-top |

## CSS Variables (styles.css :root)

Never hardcode colors or fonts inline — use these:

| Variable | Value | Use |
|---|---|---|
| `--color-primary` | `#1a4d8f` | Dark blue — main brand color |
| `--color-secondary` | `#e67e22` | Orange — accents, highlights |
| `--color-battery` | `#27ae60` | Green — battery/ASSB research |
| `--color-synchrotron` | `#9b59b6` | Purple — operando/synchrotron |
| `--font-display` | Inter, Noto Sans TC | Body and headings |
| `--font-mono` | JetBrains Mono | Code-style text |

## Patterns & Conventions

- **BEM-like class naming**: `.research-card`, `.team-member`, `.publication-list`, etc.
- **Filtering**: `data-category` attributes on news items and gallery photos; JS in `script.js` handles filtering
- **Tabs**: `data-tab` attributes on people page for PI / Members / Alumni switching
- **Mobile breakpoint**: 768px (hamburger menu kicks in below this)
- **Semantic HTML5**: `<nav>`, `<main>`, `<section>`, `<article>` throughout
- **Navigation**: Hardcoded in every HTML file — update all 7 pages when adding a new nav item

## Common Editing Tasks

**Add a team member** (`people.html`):
- Copy an existing `.team-member` div block in the appropriate tab
- Update name, role, research focus, email, photo src
- Add photo to `image/`

**Add a publication** (`publications.html`):
- Find the correct year group (`<div class="year-group">`)
- Copy an existing publication entry and update all fields
- Update the total publication count in the stats section

**Add a news item** (`index.html`):
- Copy an existing `.news-item` div
- Set `data-category` to one of: `award`, `publication`, `event`, `milestone`
- Add date and description

**Change colors or fonts**:
- Edit CSS custom properties in `styles.css :root` — affects entire site

## Notes

- **Never run `git commit` or `git push`** — always ask for permission first; user handles all commits and pushes
- Google Fonts loaded via CDN (Inter, Noto Sans TC, JetBrains Mono)
- `image/` contains: `Ben.JPG`, equipment photos, `cip.svg`, `placeholder.jpg`
