# -*- coding: utf-8 -*-
"""Batch convert md files to styled HTML pages."""
import re, os, glob
import markdown

SRC = r"C:\Users\YAN Qiongxiang\Desktop\两万三"
OUT = os.path.join(SRC, "html")
os.makedirs(OUT, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; line-height: 1.8;
         max-width: 860px; margin: 0 auto; padding: 24px; color: #2c3e50; background: #fdfdfd; }}
  h1 {{ color: #1a5276; border-bottom: 3px solid #1a5276; padding-bottom: 8px; }}
  h2 {{ color: #21618c; margin-top: 1.6em; border-bottom: 1px solid #d5dbdb; padding-bottom: 4px; }}
  h3 {{ color: #2874a6; }}
  blockquote {{ background: #f4f6f7; border-left: 4px solid #2874a6; margin: 1em 0;
               padding: 8px 16px; color: #566573; }}
  code {{ background: #f2f3f4; padding: 2px 5px; border-radius: 3px; }}
  pre code {{ display: block; padding: 12px; overflow-x: auto; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
  th, td {{ border: 1px solid #ccd1d1; padding: 6px 10px; text-align: left; }}
  th {{ background: #eaf2f8; }}
  a {{ color: #21618c; }}
  .nav {{ text-align: right; margin-bottom: 8px; }}
</style>
</head>
<body>
<div class="nav"><a href="index.html">← 返回目录</a></div>
{body}
<hr>
<small>终极 23000 单词 · 主题故事合集</small>
</body>
</html>
"""

md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"])

def convert(path, outname=None):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)  # strip front matter
    # rewrite links pointing to .md -> .html
    text = re.sub(r"\]\((\./)?([^)#]+)\.md", r"](\2.html", text)
    md.reset()
    body = md.convert(text)
    title = os.path.basename(path)[:-3] if path.endswith(".md") else outname
    out = os.path.join(OUT, outname or (os.path.basename(path)[:-3] + ".html"))
    with open(out, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(title=title, body=body))

files = glob.glob(os.path.join(SRC, "Topic*.md")) + \
        [os.path.join(SRC, "index.md"), os.path.join(SRC, "README.md")]
for p in sorted(files):
    convert(p)
    print("OK", os.path.basename(p))
print("total:", len(files))
