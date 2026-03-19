import os
import glob
import re


def create_dist_dirs():
    os.makedirs("dist/fastapi", exist_ok=True)
    os.makedirs("dist/docker", exist_ok=True)


def extract_title(html_content):
    m_h2 = re.search(r"<h2.*?>([\s\S]*?)</h2>", html_content)
    if m_h2:
        return m_h2.group(1).strip()
    return "Chapter"


def generate_handbook(src_dir, dist_folder, book_title):
    css_path = os.path.join(src_dir, "styles.css")
    cover_path = os.path.join(src_dir, "cover.html")

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    with open(cover_path, "r", encoding="utf-8") as f:
        cover = f.read()

    chapter_files = sorted(glob.glob(os.path.join(src_dir, "chapters", "*.html")))

    # 1. Autogenerate TOC HTML based on discovered chapters
    toc_links = []
    chapters_data = []

    for i, cf in enumerate(chapter_files):
        filename = os.path.basename(cf)  # e.g. chapter_01.html
        with open(cf, "r", encoding="utf-8") as f:
            content = f.read()
        title = extract_title(content)
        chapters_data.append({"filename": filename, "title": title, "content": content})
        toc_links.append(f'<li><a href="{filename}">{title}</a></li>')

    toc_html = '<ul class="toc-list">\n' + "\n".join(toc_links) + "\n</ul>"

    # Base layout template
    def render_page(content_html, current_idx=None):
        nav_buttons = ""
        if current_idx is not None:
            prev_btn = (
                f'<a href="{chapters_data[current_idx-1]["filename"]}" class="nav-btn">← Previous</a>'
                if current_idx > 0
                else f'<a href="index.html" class="nav-btn">← Cover</a>'
            )
            next_btn = (
                f'<a href="{chapters_data[current_idx+1]["filename"]}" class="nav-btn">Next →</a>'
                if current_idx < len(chapters_data) - 1
                else '<a href="#" class="nav-btn disabled">End of Handbook</a>'
            )
            nav_buttons = f'<div class="nav-buttons">{prev_btn}{next_btn}</div>'
        else:
            # We are on the cover page
            start_btn = (
                f'<a href="{chapters_data[0]["filename"]}" class="nav-btn">Start Reading →</a>'
                if chapters_data
                else ""
            )
            nav_buttons = f'<div class="nav-buttons">{start_btn}</div>'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="layout">
        <nav class="sidebar">
            <h3>Table of Contents</h3>
            {toc_html}
        </nav>
        <main class="content-wrapper">
            {content_html}
            {nav_buttons}
        </main>
    </div>
</body>
</html>"""

    # Write Cover/Index
    with open(
        os.path.join("dist", dist_folder, "index.html"), "w", encoding="utf-8"
    ) as f:
        f.write(render_page(cover))

    # Write Chapters
    for i, chap in enumerate(chapters_data):
        with open(
            os.path.join("dist", dist_folder, chap["filename"]), "w", encoding="utf-8"
        ) as f:
            f.write(render_page(chap["content"], i))


def build_hub():
    hub_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Developer Handbooks Hub</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: #0a0a0a; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        h1 { font-size: 3rem; margin-bottom: 50px; color: #0db7ed; }
        .grid { display: flex; gap: 30px; }
        .card { background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 40px; width: 300px; text-align: center; text-decoration: none; color: #fff; transition: transform 0.2s, border-color 0.2s; }
        .card:hover { transform: translateY(-5px); }
        .fastapi:hover { border-color: #009688; box-shadow: 0 10px 20px rgba(0, 150, 136, 0.2); }
        .docker:hover { border-color: #0db7ed; box-shadow: 0 10px 20px rgba(13, 183, 237, 0.2); }
        h2 { margin: 0 0 15px 0; }
        p { color: #aaa; line-height: 1.5; }
    </style>
</head>
<body>
    <h1>Developer Handbook Hub</h1>
    <div class="grid">
        <a href="/fastapi/" class="card fastapi">
            <h2 style="color: #009688;">FastAPI Notes</h2>
            <p>Everything you need to build, scale, and secure FastAPI backends natively.</p>
        </a>
        <a href="/docker/" class="card docker">
            <h2 style="color: #0db7ed;">Docker Notes</h2>
            <p>The definitive cheat-sheet-meets-deep-dive that developers keep open.</p>
        </a>
    </div>
</body>
</html>"""
    with open(os.path.join("dist", "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)


if __name__ == "__main__":
    create_dist_dirs()
    print("Building FastAPI Handbook...")
    generate_handbook("src_fastapi", "fastapi", "FastAPI Complete Handbook")
    print("Building Docker Handbook...")
    generate_handbook("src_docker", "docker", "Docker for Developers")
    print("Building Hub...")
    build_hub()
    print("Successfully compiled SSG to /dist/")
