# CJHuang Group Website - Setup Instructions

**Updated with your actual CV information!**

## What's New

✅ Your actual name: **Chen-Jui (Ben) Huang**  
✅ Current position: **Incoming Assistant Professor (Starting August 2026)**  
✅ Real publications from your CV (62+ publications)  
✅ Accurate biography with UChicago, Argonne, Stanford experience  
✅ Updated research interests matching your actual expertise  

## Files Included

Your new professional website includes:
- `index.html` - Homepage with mission and latest news
- `research.html` - Detailed research areas page
- `people.html` - Team members page  
- `publications.html` - Publications list
- `join.html` - Join us / recruitment page
- `styles.css` - All styling for the website
- `script.js` - Interactive features (carousel, smooth scrolling)

## How to Upload to GitHub Pages

### Method 1: Upload Directly on GitHub (Easiest)

1. Go to your repository: https://github.com/bencjhuang/bencjhuang.github.io

2. **Delete old files** (or move them to a backup folder):
   - Click on `index.md` → click trash icon → commit deletion
   - Repeat for `_config.yml`, `join.md`, `people.md`, `publications.md`, `research.md`

3. **Upload new files**:
   - Click "Add file" → "Upload files"
   - Drag and drop ALL 7 files (the 5 HTML files, styles.css, and script.js)
   - Commit changes

4. Wait 1-2 minutes, then visit: https://bencjhuang.github.io

### Method 2: Using Git Command Line

```bash
# Clone your repository
git clone https://github.com/bencjhuang/bencjhuang.github.io.git
cd bencjhuang.github.io

# Delete old files
rm index.md _config.yml join.md people.md publications.md research.md README.md

# Copy new files into the repository folder
# (copy all 7 files from your downloads into this folder)

# Add and commit
git add .
git commit -m "Update website with new professional design"
git push origin main
```

## Customization Guide

### 1. Adding Your Photos

**For team member photos**, find this code in `people.html`:

```html
<div class="photo-placeholder">👨‍🔬</div>
```

Replace with:
```html
<img src="YOUR_IMAGE_URL_HERE.jpg" alt="Name" style="width:100%; height:100%; object-fit:cover;">
```

**For hero carousel backgrounds**, edit `styles.css` around line 85:

```css
.hero-slide:nth-child(1) {
    background-image: url('YOUR_LAB_PHOTO_URL.jpg');
    background-size: cover;
    background-position: center;
}
```

### 2. Updating Content

**News Items** (index.html, line ~170):
```html
<div class="news-item">
    <div class="news-date">Feb 2026</div>
    <h3>Your News Title</h3>
    <p>Your news content...</p>
    <span class="news-category">CATEGORY</span>
</div>
```

**Team Members** (people.html, line ~60):
- Just copy and paste the team-member div block
- Update name, role, research focus, and email

**Publications** (publications.html, line ~80):
- Copy and paste publication div blocks
- Update title, authors, venue, year

### 3. Changing Colors

Edit the top of `styles.css`:

```css
:root {
    --color-primary: #1a4d8f;    /* Main blue color */
    --color-secondary: #e67e22;  /* Orange accent */
    --color-battery: #27ae60;    /* Green for battery tags */
    --color-synchrotron: #9b59b6; /* Purple for synchrotron */
}
```

### 4. Adding More Pages

To add a new page:
1. Copy one of the existing HTML files
2. Update the content
3. Add a link in the navigation menu (update all 5 HTML files)

## Tips

- All pages share the same `styles.css` and `script.js`
- Keep all files in the root directory of your repository
- Images should be hosted online (use GitHub, Imgur, or image hosting service)
- Test locally by opening `index.html` in your browser before uploading

## Need Help?

- GitHub Pages Documentation: https://docs.github.com/en/pages
- Contact: Your friendly AI assistant (Claude) 😊

## Quick Checklist

- [ ] Upload all 7 files to GitHub repository
- [ ] Delete old .md files
- [ ] Wait 1-2 minutes for GitHub Pages to update
- [ ] Visit https://bencjhuang.github.io to see your new site
- [ ] Customize content (team members, publications, photos)
- [ ] Add your actual photos
- [ ] Update contact information
- [ ] Share with your team!

---

**Note:** Your site will be live at https://bencjhuang.github.io immediately after uploading. You can always update individual files later by editing them directly on GitHub or pushing changes via git.
