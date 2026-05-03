# bencjhuang.github.io

Academic group website for the **CJHuang Group** (Prof. Chen-Jui "Ben" Huang) at
National Taiwan University of Science and Technology — starting August 2026.

Static site, no build step. Edit HTML/CSS/JS directly, push to `main`, GitHub
Pages serves it within a minute or two.

## Local development

```bash
cd ~/Documents/GitHub/bencjhuang.github.io
python3 -m http.server 8000
```

Open <http://localhost:8000>. Hard-refresh (`Cmd+Shift+R`) after edits to bypass
the browser cache.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Homepage — hero, mission, three research preview cards, news, quick-nav |
| `research.html` | Four research areas (ASSB, anode-free, operando, XCT) with sticky sidebar ToC |
| `people.html` | Tabs: PI · Members (open project areas) · Alumni |
| `publications.html` | 65+ peer-reviewed articles, conferences, patents · year/type filter chips · search |
| `equipment.html` | Planned in-house instrumentation + synchrotron access (NSRRC, APS) |
| `gallery.html` | Filterable photo grid with full-screen lightbox |
| `join.html` | Open positions and how to apply |

## Design system

All design tokens live in `:root` at the top of `styles.css`. **Never hardcode
colors or fonts in markup** — use these variables.

### Palette — single accent

| Token | Value | Use |
|---|---|---|
| `--ink` | `#0B1220` | Near-black navy — primary text + UI |
| `--ink-soft` | `#1f2a3d` | Secondary text |
| `--paper` | `#FAFAF7` | Warm off-white background |
| `--surface` | `#FFFFFF` | Cards, elevated surfaces |
| `--rule` | `#E5E7EB` | Hairline borders |
| `--muted` | `#6B7280` | Tertiary text |
| `--accent` | `#C2410C` | Terracotta — single accent (CTAs, eyebrows, link hover, bars) |
| `--accent-2` | `#9A330A` | Hover-deeper accent |

### Type

| Token | Family | Use |
|---|---|---|
| `--font-display` | Fraunces (serif) | H1, H2, H3 — editorial gravity |
| `--font-body` | Inter | Body text, UI |
| `--font-mono` | JetBrains Mono | Eyebrows, dates, tags, technical labels |

### Motion

- Standard easing: `cubic-bezier(0.22, 1, 0.36, 1)` via `--ease`
- Card hover: `translateY(-6px)` + shadow lift + accent bar slide-in
- All animations respect `prefers-reduced-motion`

## Common edits

### Change the palette

Edit `--accent` in `styles.css :root`. Everything terracotta updates site-wide.

### Add a publication

Find the right `<div class="year-group" data-year="YYYY">` in
`publications.html` and copy an existing `<div class="publication">` block:

```html
<div class="publication">
    <div class="pub-title"><a href="DOI" target="_blank">TITLE</a></div>
    <div class="pub-authors">AUTHORS — wrap your name in <strong>C.-J. Huang</strong></div>
    <div class="pub-venue">Journal Name <span class="pub-year">YYYY</span><span class="pub-impact">IF: NN.N</span></div>
</div>
```

The numbering counter is **automatic** — JS counts pubs on load and assigns
`data-num` attributes. No CSS counter to keep in sync.

Update the stat counts in the `pub-stats` block at the top of the page.

### Add a news item

In `index.html`, copy an existing `<article class="news-item">` block:

```html
<article class="news-item" data-category="announcement">
    <div class="news-date">MMM YYYY</div>
    <div>
        <h3>Title</h3>
        <p>Body</p>
        <span class="badge-cat announcement">Announcement</span>
    </div>
</article>
```

`data-category` values: `announcement`, `award`, `publication`, `activity`.

### Add a gallery photo

In `gallery.html`, copy an existing `<article class="gallery-item">` block:

```html
<article class="gallery-item" data-category="lab">
    <img loading="lazy" decoding="async" src="image/your-photo.jpg" alt="Description">
    <div class="gallery-caption">
        <span class="gallery-caption__tag">Lab</span>
        <p>Caption.</p>
    </div>
</article>
```

`data-category` values: `lab`, `research`, `conference`, `group`. The lightbox
picks it up automatically.

### Add a navigation item

The nav is hardcoded in every HTML file. If you add a page, update the `<nav>`
and `.mobile-menu` blocks in **all 7 pages**.

## Image conventions

Drop new images into `image/`. For consistent rendering:

| Use | Pattern |
|---|---|
| Hero / wide photos | landscape, ≥2400px wide, JPG quality 80–85 |
| Research figures | wide aspect (2:1 or 3:2), white or transparent bg if possible |
| Equipment photos | 3:2 or close, real photos better than stock |
| OG / share image | `image/og-default.jpg` — 1200×630 |

Originals of the compressed hero and operando files are kept in
`image/_originals/` if you ever need to regenerate.

## Cache busting

If you replace an image at the same filename and the browser keeps showing the
old one, append `?v=N` to the `src` URL — increment `N` every time you swap.
The server ignores the query string; the browser treats it as a new resource.

## Workflow

The site is on the `redesign` branch. To deploy:

```bash
git checkout main
git merge redesign
git push origin main
```

GitHub Pages will pick up the change in ~1 minute.

To preview the old version:

```bash
git checkout main      # original
git checkout redesign  # current
```

## Files

```
.
├── index.html         # Homepage
├── research.html      # Research areas + sticky ToC
├── people.html        # PI, members, alumni
├── publications.html  # Filterable publication list
├── equipment.html     # Facilities + synchrotron access
├── gallery.html       # Filterable photo grid + lightbox
├── join.html          # Open positions
├── styles.css         # All styles — single source of truth
├── script.js          # Reveal-on-scroll, filters, lightbox, ToC, hamburger
├── image/
│   ├── og-default.jpg          # Social card image (1200×630)
│   ├── hero-beamline.jpg       # Homepage hero
│   ├── research-*.jpg          # Research card figures
│   ├── Ben.JPG                 # PI portrait
│   ├── g-*.jpg / *.png / cip.svg # Equipment photos
│   └── _originals/             # Pre-compression backups
└── CLAUDE.md          # Project notes for AI editing
```
