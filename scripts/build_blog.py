#!/usr/bin/env python3
"""Build the static On Psyduck article. Standard-library Python; no packages needed."""
import argparse
import base64
import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "blog" / "on-psyduck"
SOURCE = ARTICLE / "article.md"
LOGO = ROOT / "assets" / "bidextool-logo.png"

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def inline(value):
    tokens = []
    def keep(markup):
        tokens.append(markup)
        return "ZZTOKEN" + str(len(tokens) - 1) + "ZZ"
    value = re.sub(r"\[\\\[(\d+)\\\]\]\(#ref-(\d+)\)",
        lambda m: keep('<sup class="citation"><a href="#ref-' + m[2] +
        '" aria-label="Reference ' + m[1] + '">[' + m[1] + ']</a></sup>'), value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: keep('<a href="' + html.escape(m[2], quote=True) + '">' +
        html.escape(m[1]) + "</a>"), value)
    value = html.escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*(.+?)\*", r"<em>\1</em>", value)
    value = value.replace("\n", " ")
    for i, token in enumerate(tokens):
        value = value.replace("ZZTOKEN" + str(i) + "ZZ", token)
    return value

CSS = """
:root{color-scheme:light;--ink:#20252e;--muted:#626975;--navy:#1e3a8a;--line:#e6e7e9;--paper:#fffdfa;--accent:#e9b83b}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:36px}body{margin:0;background:var(--paper);color:var(--ink);font-family:Georgia,"Times New Roman",serif;-webkit-font-smoothing:antialiased}
a{color:var(--navy);text-decoration-thickness:1px;text-underline-offset:3px}a:hover{text-decoration-color:var(--accent)}a:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:5px;border-radius:2px}
.site-nav{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;max-width:1060px;margin:auto;padding:23px 32px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:16px;font-size:13px}
.site-nav a{text-decoration:none;font-weight:600}.site-nav span{color:var(--muted)}
main{max-width:764px;margin:0 auto;padding:58px 32px 72px}
.article-header{text-align:center}.eyebrow{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;text-transform:uppercase;letter-spacing:.18em;font-size:11px;color:var(--navy);font-weight:650;margin:0 0 18px}
h1{font-size:clamp(48px,8vw,70px);font-weight:500;letter-spacing:-.045em;line-height:1.07;margin:0 0 18px}.subtitle{font-size:19px;color:#4c5361;line-height:1.5;margin:0 auto 19px;max-width:550px}
.chinese-title{display:block;font-family:"Noto Serif CJK SC","Songti SC",SimSun,serif;font-size:.46em;letter-spacing:.09em;line-height:1.35;margin-top:.38em}
.byline{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:13px;color:var(--muted);line-height:1.8;margin:0}.byline a{color:var(--ink);text-decoration:none;white-space:nowrap}.byline .author-chinese{font-size:.95em;margin-left:.35em}.byline .dot{padding:0 8px}.byline time{white-space:nowrap}
.logo-figure{margin:32px auto 38px;text-align:center}.logo-figure img{display:block;width:240px;max-width:65%;height:auto;margin:auto}
.recording-links{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;text-align:center;font-size:14px;line-height:1.7;margin:0 0 34px;padding:16px 18px;background:#f4f5f7;border:1px solid var(--line);border-radius:8px}.recording-links strong{display:block;margin-bottom:8px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}.recording-links a{display:inline-block;padding:7px 16px;border:1px solid #cbd3e1;border-radius:5px;background:#fff;text-decoration:none;font-weight:600}.recording-links a:hover{border-color:var(--navy);background:#eef2fa}
.article-body{font-size:19px;line-height:1.8}.article-body p{margin:0 0 22px}.article-body>p:first-child{font-size:21px;line-height:1.75}
h2{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:26px;line-height:1.35;letter-spacing:-.025em;font-weight:650;margin:54px 0 22px;color:#172942;text-wrap:balance}
hr{border:0;border-top:1px solid var(--line);margin:42px 0}strong{font-weight:700}
.citation{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:11px;line-height:0;vertical-align:super;white-space:nowrap;margin-left:2px}.citation a{text-decoration:none}
.cliffhanger{border-left:3px solid var(--accent);padding:6px 0 6px 23px;margin:30px 0;font-size:25px;line-height:1.55;color:#172942}
.references{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:13px;line-height:1.75;border-top:1px solid var(--line);padding-top:14px;margin-top:48px}.references h2{font-size:21px;margin-top:24px}
.references p{margin-bottom:17px}.references .time{display:block;color:var(--muted);font-variant-numeric:tabular-nums;margin-top:2px}
.reference-entry:target{background:#fff0bf;outline:8px solid #fff0bf;border-radius:2px}
.editing-credit{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:12px;color:var(--muted);line-height:1.7;margin-top:34px}
footer{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:18px;border-top:1px solid var(--line);padding-top:20px;margin-top:30px}
@media(max-width:540px){.site-nav{padding:18px 22px;font-size:12px}.site-nav span{display:none}main{padding:38px 23px 48px}.article-body{font-size:18px;line-height:1.8}.article-body>p:first-child{font-size:19px}.subtitle{font-size:17px}h2{font-size:23px;margin-top:42px}.logo-figure img{width:195px}.logo-figure{margin:28px auto 30px}.cliffhanger{font-size:22px;padding-left:18px}footer{flex-wrap:wrap}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:#fff}main{max-width:none;padding:0}.site-nav,footer{display:none}.logo-figure img{width:150px}.article-body{font-size:11pt;line-height:1.6}h1{font-size:36pt}h2{font-size:16pt;break-after:avoid}.references{font-size:9pt}.cliffhanger{font-size:15pt}a{color:inherit}.reference-entry{break-inside:avoid}}
"""

def build(standalone=False):
    md = SOURCE.read_text(encoding="utf-8")
    parts = md.strip().split("\n\n")
    assert parts[0].startswith("# On Psyduck")
    english_title = parts.pop(0)[2:]
    assert parts[0].startswith("### ")
    chinese_title = parts.pop(0)[4:]
    title = english_title + " | " + chinese_title
    title_markup = (html.escape(english_title) +
        '<span class="chinese-title" lang="zh-Hans">' + html.escape(chinese_title) + '</span>')
    meta = parts.pop(0).splitlines()
    subtitle = meta[0].strip(" *")
    author = meta[1].strip(" *")
    author_name, published_date = author.split(" · ", 1)
    author_markup = html.escape(author_name).replace(" 李润发", ' <span class="author-chinese" lang="zh-Hans">李润发</span>')
    published_iso = datetime.strptime(published_date, "%B %d, %Y").date().isoformat()
    assert parts.pop(0).startswith("![BiDexTool logo")
    recording = parts.pop(0)
    assert recording.startswith("**Full workshop recording:**")
    body = []
    in_refs = False
    ref_id = None
    for part in parts:
        part = part.strip()
        if part.startswith("## "):
            heading = part[3:]
            if heading == "References and timestamps":
                body.append('<section class="references" aria-labelledby="references-and-timestamps">')
                in_refs = True
            body.append('<h2 id="' + slug(heading) + '">' + html.escape(heading) + '</h2>')
        elif part == "---":
            if in_refs:
                body.append("</section>")
                in_refs = False
            else:
                body.append("<hr>")
        elif re.fullmatch(r'<a id="ref-\d+"></a>', part):
            ref_id = re.search(r'ref-\d+', part)[0]
        elif part.startswith("*Editing assistance:"):
            body.append('<p class="editing-credit">' + inline(part.strip("*")) + "</p>")
        elif part.startswith("“Ask me again in three years."):
            body.append('<blockquote class="cliffhanger">' + inline(part) + "</blockquote>")
        elif ref_id:
            ref_title, times = part.split("** ", 1)
            body.append('<p class="reference-entry" id="' + ref_id + '">' +
                inline(ref_title + "**") + '<span class="time">' + html.escape(times) + "</span></p>")
            ref_id = None
        else:
            body.append("<p>" + inline(part) + "</p>")
    if in_refs:
        body.append("</section>")
    logo = "../../assets/bidextool-logo.png"
    home = "../../index.html"
    if standalone:
        logo = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode("ascii")
        home = "https://bimanual-tool.github.io/"
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>""" + html.escape(title) + """ - Runfa Blark Li | BiDexTool 2026</title>
<meta name="description" content="Two hands, a paintbrush, and a few questions from CoRL 2026. Runfa Blark Li reflects on generalization, contact, and the future of dexterous tool use.">
<meta name="author" content="Runfa Blark Li 李润发">
<meta name="theme-color" content="#fffdfa">
<link rel="canonical" href="https://bimanual-tool.github.io/blog/on-psyduck/">
<meta property="og:type" content="article">
<meta property="og:title" content=\"""" + html.escape(title, quote=True) + """\">
<meta property="article:published_time" content=\"""" + published_iso + """\">
<meta property="og:description" content="Two hands, a paintbrush, and a few questions from CoRL 2026.">
<meta property="og:url" content="https://bimanual-tool.github.io/blog/on-psyduck/">
<meta property="og:site_name" content="BiDexTool · CoRL 2026">
<meta property="og:image" content="https://bimanual-tool.github.io/assets/on-psyduck-social.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="On Psyduck / 论·可达鸭 — a BiDexTool workshop reflection, with the two-handed Psyduck painting mascot.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="On Psyduck | 论·可达鸭">
<meta name="twitter:description" content="A workshop reflection by Runfa Blark Li: two hands, a paintbrush, and a few questions from CoRL 2026.">
<meta name="twitter:image" content="https://bimanual-tool.github.io/assets/on-psyduck-social.png">
<meta name="twitter:image:alt" content="On Psyduck / 论·可达鸭 — BiDexTool at CoRL 2026, with the workshop mascot.">
<style>""" + CSS + """</style>
</head>
<body>
<nav class="site-nav" aria-label="Workshop navigation">
<a href=\"""" + home + """\">← BiDexTool workshop</a>
<span>CoRL 2026 · Austin</span>
<a href="#references-and-timestamps">References</a>
</nav>
<main id="top">
<article>
<header class="article-header">
<p class="eyebrow">A workshop reflection</p>
<h1>""" + title_markup + """</h1>
<p class="subtitle">""" + html.escape(subtitle) + """</p>
<p class="byline"><a href="https://blarklee.github.io/">""" + author_markup + """</a><span class="dot">·</span><time datetime=\"""" + published_iso + """\">""" + html.escape(published_date) + """</time></p>
</header>
<figure class="logo-figure">
<img src=\"""" + logo + """\" width="1186" height="1327" alt="BiDexTool logo: two robotic hands holding and painting a Psyduck figurine" fetchpriority="high">
</figure>
<nav class="recording-links" aria-label="Full workshop recording">""" + inline(recording) + """</nav>
<div class="article-body">
""" + "\n".join(body) + """
</div>
</article>
<footer><span>BiDexTool · CoRL 2026</span><a href="#top">Back to top ↑</a></footer>
</main>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--standalone", type=Path, help="Also export one HTML file with the logo embedded.")
    args = parser.parse_args()
    target = ARTICLE / "index.html"
    target.write_text(build(), encoding="utf-8")
    print("Built " + str(target))
    if args.standalone:
        args.standalone.parent.mkdir(parents=True, exist_ok=True)
        args.standalone.write_text(build(standalone=True), encoding="utf-8")
        print("Exported " + str(args.standalone))

if __name__ == "__main__":
    main()
