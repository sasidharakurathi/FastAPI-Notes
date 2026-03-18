import os
import glob


def build_handbook():
    src_dir = "src"
    dist_file = "index.html"

    # Read CSS
    with open(os.path.join(src_dir, "styles.css"), "r", encoding="utf-8") as f:
        css = f.read()

    # Read cover
    with open(os.path.join(src_dir, "cover.html"), "r", encoding="utf-8") as f:
        cover = f.read()

    # Read toc
    with open(os.path.join(src_dir, "toc.html"), "r", encoding="utf-8") as f:
        toc = f.read()

    # Read chapters
    chapters_dir = os.path.join(src_dir, "chapters")
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.html")))

    chapters_content = ""
    for cf in chapter_files:
        with open(cf, "r", encoding="utf-8") as f:
            chapters_content += f.read() + "\n"

    # Read JS
    with open(os.path.join(src_dir, "script.js"), "r", encoding="utf-8") as f:
        js_script = f.read()

    html_template = f"""<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta name="description" content="A complete FastAPI handbook covering every concept with real examples, from basics to production deployment.">
                <meta name="author" content="Sasidhar Akurathi">
                <meta property="og:title" content="FastAPI Complete Handbook">
                <meta property="og:description" content="Every concept. Every feature. With real examples. Based on official FastAPI docs.">
                <meta property="og:type" content="article">
                <title>FastAPI Complete Handbook</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/atom-one-light.min.css">
                <style>
                    {css}
                </style>
            </head>
            <body>

                <div class="progress-bar" id="progress-bar"></div>

                {cover}

                {toc}

                {chapters_content}

                <div id="link-status" class="link-status" aria-hidden="true"></div>

                <div class="floating-controls" aria-label="Page navigation controls">
                    <button id="btn-prev-page" type="button" class="floating-btn">Prev Page</button>
                    <button id="btn-next-page" type="button" class="floating-btn">Next Page</button>
                    <button id="btn-top" type="button" class="floating-btn floating-btn-top">Top</button>
                </div>

                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/languages/python.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/languages/bash.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/languages/json.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/languages/dockerfile.min.js"></script>
                <script>
                    document.querySelectorAll('pre').forEach(function(pre) {{
                        if (!pre.querySelector('code')) {{
                            var code = document.createElement('code');
                            code.className = 'language-python';
                            code.textContent = pre.textContent;
                            pre.textContent = '';
                            pre.appendChild(code);
                        }}
                        var wrapper = document.createElement('div');
                        wrapper.className = 'code-wrapper';
                        pre.parentNode.insertBefore(wrapper, pre);
                        wrapper.appendChild(pre);
                        var btn = document.createElement('button');
                        btn.className = 'copy-btn';
                        btn.textContent = 'Copy';
                        btn.type = 'button';
                        btn.addEventListener('click', function() {{
                            var text = pre.textContent || '';
                            navigator.clipboard.writeText(text).then(function() {{
                                btn.textContent = 'Copied!';
                                btn.classList.add('copied');
                                setTimeout(function() {{
                                    btn.textContent = 'Copy';
                                    btn.classList.remove('copied');
                                }}, 1500);
                            }});
                        }});
                        wrapper.appendChild(btn);
                    }});
                    hljs.highlightAll();
                </script>

                <script>
                    {js_script}
                </script>

            </body>
        </html>
    """

    with open(dist_file, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Successfully built {dist_file}")


if __name__ == "__main__":
    build_handbook()
