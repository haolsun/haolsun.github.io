#!/usr/bin/env python3
"""Fetch a key figure for each publication and rewrite blocks to paper-box.
Fixed: replacements applied back-to-front to avoid index corruption.
Images already on disk are reused (no re-download)."""
import os, re, io
import requests
from urllib.parse import urljoin, quote
import fitz  # PyMuPDF
from PIL import Image

BASE = r"C:\Users\haols\WorkBuddy\2026-07-19-10-33-47\new-site"
HTML = os.path.join(BASE, "index.html")
IMG_DIR = os.path.join(BASE, "assets", "img", "pubs")
os.makedirs(IMG_DIR, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
S = requests.Session()
S.headers.update(UA)

def get(url, timeout=25, headers=None):
    h = dict(UA)
    if headers:
        h.update(headers)
    try:
        return S.get(url, timeout=timeout, headers=h)
    except Exception as e:
        print(f"  ! GET failed {url[:80]}: {e}")
        return None

# ---------- image extraction ----------
def github_teaser(repo_url):
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
    if not m:
        return None
    owner, name = m.group(1), m.group(2).replace(".git", "")
    for branch in ("main", "master"):
        for fn in ("README.md", "README.markdown", "README.rst", "readme.md"):
            raw = f"https://raw.githubusercontent.com/{owner}/{name}/{branch}/{fn}"
            r = get(raw)
            if not r or r.status_code != 200:
                continue
            text = r.text
            refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
            refs += re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", text)
            base_raw = f"https://raw.githubusercontent.com/{owner}/{name}/{branch}/"
            for ref in refs:
                if ref.startswith("data:"):
                    continue
                img_url = ref if ref.startswith("http") else urljoin(base_raw, ref.lstrip("/"))
                ir = get(img_url)
                if not ir or ir.status_code != 200:
                    continue
                if len(ir.content) < 1500:
                    continue
                return ir.content
    return None

def pdf_largest_figure(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        print(f"  ! PDF open failed: {e}")
        return None
    best, best_area = None, 0
    for page in doc:
        for img in page.get_images(full=True):
            try:
                info = doc.extract_image(img[0])
            except Exception:
                continue
            w, h = info.get("width"), info.get("height")
            if not w or not h or w < 220 or h < 220:
                continue
            area = w * h
            if area > best_area:
                best_area, best = area, info["image"]
    doc.close()
    return best

def arxiv_pdf(arxiv_id):
    r = get(f"https://arxiv.org/pdf/{arxiv_id}")
    if r and r.status_code == 200:
        return pdf_largest_figure(r.content)
    return None

def other_pdf(pdf_url, referer=None):
    r = get(pdf_url, timeout=30, headers={"Referer": referer} if referer else None)
    if r and r.status_code == 200 and r.content.startswith(b"%PDF"):
        return pdf_largest_figure(r.content)
    return None

def arxiv_by_title(title):
    q = quote(title)
    r = get(f"http://export.arxiv.org/api/query?search_query=ti:%22{q}%22&max_results=1")
    if r and r.status_code == 200:
        m = re.search(r"<id>https?://arxiv\.org/abs/([^<]+)</id>", r.text)
        if m:
            return m.group(1)
    return None

def cvf_direct(block):
    m = re.search(r"openaccess\.thecvf\.com(?::\d+)?/([^\"\s]+)", block)
    if m:
        return other_pdf("https://openaccess.thecvf.com/" + m.group(1))
    return None

def save_image(data, slug):
    try:
        img = Image.open(io.BytesIO(data))
    except Exception:
        ext = "svg" if data.lstrip().startswith(b"<svg") else "png"
        fn = f"{slug}.{ext}"
        open(os.path.join(IMG_DIR, fn), "wb").write(data)
        return fn
    img = img.convert("RGB")
    if img.width > 520:
        img = img.resize((520, int(img.height * 520 / img.width)), Image.LANCZOS)
    fn = f"{slug}.png"
    img.save(os.path.join(IMG_DIR, fn), "PNG", optimize=True)
    return fn

def existing(slug):
    for ext in ("png", "svg"):
        p = os.path.join(IMG_DIR, f"{slug}.{ext}")
        if os.path.exists(p):
            return f"{slug}.{ext}"
    return None

# ---------- parse blocks (balanced divs) ----------
def find_pub_blocks(html):
    blocks, i = [], 0
    while True:
        m = html.find('<div class="pub">', i)
        if m == -1:
            break
        depth, end = 0, None
        for tag in re.finditer(r"<div\b|</div>", html[m:]):
            if tag.group() == "<div":
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = m + tag.end()
                    break
        if end is None:
            break
        blocks.append((m, end, html[m:end]))
        i = end
    return blocks

html = open(HTML, encoding="utf-8").read()
blocks = find_pub_blocks(html)
print(f"Found {len(blocks)} pub blocks (incl. comment placeholder)")

replacements = []
for (start, end, block) in blocks:
    tm = re.search(r'<div class="pub-title">(.*?)</div>', block, re.S)
    if not tm:
        continue  # skip comment placeholder
    title = tm.group(1).strip()
    bm = re.search(r'<div class="badge">(.*?)</div>', block, re.S)
    badge = re.sub(r"\s+", " ", re.sub(r"<br\s*/?>", " ", bm.group(1))).strip() if bm else ""
    arxiv_id = github_url = pdf_url = None
    for am in re.finditer(r'<a href="([^"]+)"[^>]*>([^<]*)</a>', block):
        href, label = am.group(1), am.group(2).strip().lower()
        if "arxiv.org/abs/" in href:
            arxiv_id = href.rstrip("/").split("/")[-1]
        elif "github.com" in href:
            github_url = href
        elif href.lower().endswith(".pdf") or "pdf" in href.lower() or label == "pdf":
            pdf_url = href
    slug = arxiv_id or re.sub(r"[^a-z0-9]+", "_", title.lower())[:40]
    print(f"\n* {title[:58]}  [{badge}]")

    fn = existing(slug)
    if fn:
        print(f"  -> reuse {fn}")
    else:
        data = None
        if github_url:
            data = github_teaser(github_url)
            if data: print("  -> github teaser")
        if data is None and arxiv_id:
            data = arxiv_pdf(arxiv_id)
            if data: print("  -> arxiv figure")
        if data is None and pdf_url:
            data = other_pdf(pdf_url)
            if data: print("  -> pdf figure")
        if data is None:
            aid = arxiv_by_title(title)
            if aid:
                data = arxiv_pdf(aid)
                if data: print(f"  -> arxiv(title) {aid}")
        if data is None:
            data = cvf_direct(block)
            if data: print("  -> cvf direct")
        if data is None and pdf_url:
            data = other_pdf(pdf_url, referer="https://www.google.com/")
            if data: print("  -> pdf+referer")
        if data is None:
            print("  -> NO IMAGE (text-only)")
            continue
        fn = save_image(data, slug)
        print(f"  -> saved {fn}")

    bm2 = re.search(r'<div class="pub-body">(.*)</div>\s*</div>\s*</div>', block, re.S)
    pub_body = bm2.group(1) if bm2 else ""
    new_block = (
        f'<div class="paper-box">\n'
        f'  <div class="paper-box-media">\n'
        f'    <div class="badge">{badge}</div>\n'
        f'    <div class="paper-box-image"><img src="assets/img/pubs/{fn}" alt="" loading="lazy"></div>\n'
        f'  </div>\n'
        f'  <div class="pub-body">{pub_body}</div>\n'
        f'</div>'
    )
    replacements.append((start, end, new_block))

# apply back-to-front to keep indices valid
replacements.sort(key=lambda x: x[0], reverse=True)
new_html = html
for (start, end, nb) in replacements:
    new_html = new_html[:start] + nb + new_html[end:]
open(HTML, "w", encoding="utf-8").write(new_html)

n = len(replacements)
print(f"\n=== DONE: {n} papers converted to paper-box ===")
print(f"paper-box now: {new_html.count('class=\"paper-box\"')}  pub now: {new_html.count('class=\"pub\"')}")
