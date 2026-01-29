# Theory & Computational Chemistry Group Website (GitHub Pages)

This is a lightweight static website template (English UI/content) that works directly on **GitHub Pages** (no build step).

## Folder structure

- `index.html` — Home + research directions
- `people.html` — Team members (driven by `assets/data/people.json`)
- `publications.html` — Publications (driven by `assets/data/publications.json`)
- `gallery.html` — Photos (driven by `assets/data/gallery.json`)
- `positions.html` — Open positions (driven by `assets/data/positions.json`)
- `assets/`
  - `css/style.css`
  - `js/main.js`
  - `data/*.json` (edit these)
  - `img/people/` (member photos)
  - `img/gallery/` (gallery photos)
  - `papers/` (publication PDFs)

## Quick edits

### Change group name / contact
Edit:
- Navbar brand: in each HTML file find `Your Group` and replace.
- Footer: in each HTML file find department/university/email and replace.

### Add/modify people
Edit `assets/data/people.json` and add new objects.
Put photos in `assets/img/people/` and set `photo` path accordingly.

### Add/modify publications
Edit `assets/data/publications.json`.
For each entry, optionally fill:
- `pdf`: e.g. `assets/papers/2025_my_paper.pdf`
- `url`: DOI link, publisher page, arXiv, etc.

### Add gallery photos
Put images in `assets/img/gallery/` and list them in `assets/data/gallery.json`.

## Deploy on GitHub Pages
See the step-by-step guide in the chat response.


## Publications links (permanent DOI links)

- The site displays a **single-column** publication list.
- Each entry shows its citation text, followed by inline links: **(PDF | Link)**.
- The `Link` is intended to be a **permanent DOI URL** (recommended format: `https://doi.org/<DOI>`).

### Fill missing DOI links automatically (optional)

If some `url` fields are still empty in `assets/data/publications.json`, you can auto-fetch DOIs via Crossref:

1. Make sure Python 3 is installed.
2. Install dependency:
   - `pip install requests`
3. Edit `tools/fetch_dois.py` and set `USER_AGENT` with your email.
4. Run:
   - `python tools/fetch_dois.py`

This will update `assets/data/publications.json` in place.

