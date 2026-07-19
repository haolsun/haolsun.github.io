# Haoliang Sun — Personal Homepage

A clean, responsive, single-page academic homepage built with **plain static HTML/CSS/JS**
(no Jekyll / Ruby required). Adopted the visual style of the AcadHomepage template you
forked, but rebuilt as a dependency-free static site so it is trivial to preview and deploy.

## Features
- Responsive two-column layout (sticky profile sidebar + content)
- Light / dark theme toggle (remembers your choice)
- Sections: About, News, Publications (grouped), Education, Honors, Services, Courses, People, Contact
- All real content ported from the old `haolsun.github.io` (jemdoc) site
- Your photo (`assets/img/bio.png`) and CV (`files/my_CV.pdf`) included

## Local preview
Just open `index.html` in a browser. Or serve it:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploy to GitHub Pages
This is a static site, so it works on GitHub Pages without any build step.
The included `.nojekyll` file tells GitHub **not** to run Jekyll.

### Option A — replace the existing homepage (`haolsun.github.io`)
```bash
cd new-site
git init
git add -A
git commit -m "Redesign personal homepage (static)"
git branch -M main
git remote add origin git@github.com:haolsun/haolsun.github.io.git
git push -f origin main
```
Visit https://haolsun.github.io — the address stays the same.

### Option B — use the new template repo (`haoliangsun.github.io`)
Same steps, but point the remote at `git@github.com:haolsun/haoliangsun.github.io.git`.
Note: since that repo name ≠ your username, GitHub Pages would publish it at
`https://haolsun.github.io/haoliangsun.github.io/` (a project page, not the root domain).

In **Settings → Pages**, set the source to the `main` branch (root `/`), then wait ~1 min.

## Easy edits
- **Bio / news / publications / people**: edit `index.html` (plain HTML, well-commented).
- **Colors / theme**: edit CSS variables at the top of `assets/css/style.css`.
- **Photo**: replace `assets/img/bio.png`. **CV**: replace `files/my_CV.pdf`.

## Optional: Google Scholar citation counter
The AcadHomepage Jekyll template can auto-update citation counts via a GitHub Action.
For this static version you can instead embed a shields.io badge, or keep using the
Jekyll template if you want that automation — let me know and I can set it up.
