# On Psyduck / 论·可达鸭 — 本地文件与发布说明

当前状态：文章和官网入口已在本地准备好，英文标题 On Psyduck 与中文标题 论·可达鸭 分行显示，署名为 Runfa Blark Li 李润发，日期为 November 17, 2026。尚未提交或推送到 GitHub，也尚未发布。

## 文件在哪里

本地网站仓库：
`C:\Users\blark\Desktop\Bimanual Dex tool use CoRL 2026 workshop\bimanual-tool.github.io`

| 文件 | 用途 |
| --- | --- |
| `blog/on-psyduck/article.md` | 文章正文；以后优先在这里修改文字 |
| `blog/on-psyduck/index.html` | GitHub Pages 直接提供给读者的网页 |
| `assets/bidextool-logo.png` | 沿用官网现有的可达鸭 logo |
| `scripts/build_blog.py` | 从 Markdown 生成 HTML，只需要 Python 标准库 |
| `index.html` | 已添加 Blog 导航和 On Psyduck 文章入口 |
| `blog/PUBLISHING.md` | 本说明 |

独立预览文件 `On_Psyduck.html` 内嵌了 logo 和样式。双击即可打开，不需要联网加载排版或图片。它是导出副本；正式网站使用仓库中的 `blog/on-psyduck/index.html`。

## 为什么不用申请新网页或新域名

现有官网已经通过 GitHub Pages 托管静态网页。在同一个发布目录下增加一个子目录和 `index.html`，就可以得到新页面。

计划发布地址：
https://bimanual-tool.github.io/blog/on-psyduck/

这个地址目前只是计划地址，不代表页面已经上线。它与官网共用仓库、域名和 GitHub Pages 设置。

## 如何修改和重新生成

在上述仓库目录打开 PowerShell：

```powershell
python .\scripts\build_blog.py
```

这会读取 `blog/on-psyduck/article.md` 并更新 `blog/on-psyduck/index.html`。

如需同时导出一份独立 HTML，可使用：

```powershell
python .\scripts\build_blog.py --standalone "$env:TEMP\On_Psyduck.html"
```

这个生成脚本支持本篇使用的标题、段落、强调、链接和引用格式。不要把它当成完整的通用 Markdown 渲染器。若调整引用号，请同时更新正文链接和文末对应的 `ref-N` 条目。

## 准备发布时

1. 确认正文、署名、结尾、致谢名单与引用时间。
2. 在仓库内运行 `git status --short`，确认这次包含的文件。
3. 用 `git fetch origin` 检查远程是否有新改动。如果远程 main 有更新，先合并并重新生成文章；不要强制覆盖远程。
4. 本地预览无误后，提交本次文件：

```powershell
git add index.html blog/on-psyduck/article.md blog/on-psyduck/index.html blog/PUBLISHING.md scripts/build_blog.py scripts/build_social_previews.ps1 assets/on-psyduck-social.png assets/bidextool-social.png
git commit -m "Add On Psyduck workshop reflection"
git push origin main
```

5. 在 GitHub 仓库的 Actions 页面查看 Pages 部署是否成功，再打开计划发布地址。
6. 如果更新没有自动发布，到 Settings → Pages 查看实际发布来源。现有 README 说明网站从根目录 `index.html` 提供页面；本地仓库当前分支是 main。本次没有访问或更改远程 Pages 配置。
7. 如果使用从分支部署，确保发布来源包含这些文件；如果使用 Actions，则确保部署产物包括 `blog/` 和 `assets/`。网站现有发布正常时，通常不需要改设置。

## 两种阅读版本

- ChatGPT 中原有的文章链接保留，更新同一份文稿。
- 正式网页与本地 Markdown 在本仓库内。此后修改仓库文件不会自动更新 ChatGPT 中的文稿，需要单独同步。

## 当前校验范围

已检查：HTML 结构、图片路径、14 条引用目标、正文引用编号、编辑署名、首页文章入口，以及独立导出中的 logo 字节。

已用 Chrome 打开正式网页和独立 HTML，检查 1440px 桌面与 390px 手机宽度：标题、日期、logo 和全部引用跳转正常，没有横向溢出。独立 HTML 内嵌 logo，下载后可直接双击打开。

仅运行 git push 不会上传未提交的修改；先执行上面的 git add 和 git commit。正常沿用现有 GitHub Pages 配置即可，不需要申请子网站。推送后在仓库 Actions 页面检查部署结果。

GitHub 官方说明：
https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## 录像入口与分享封面

- 导航第一项为 Reflection，位于 About 前面；标题附近有文章、YouTube、Bilibili 三个主要入口。
- 文章开头和文末时间索引处都有完整录像链接。
- YouTube：https://youtu.be/HNI-dcrl54I
- Bilibili：https://www.bilibili.com/video/BV1EVsu6QE5n/
- 文章分享封面：`assets/on-psyduck-social.png`。
- 官网分享封面：`assets/bidextool-social.png`。
- 两张封面均为 1200 × 630 PNG，使用未改动的原始 logo；网页已配置 Open Graph 和 Twitter Card 元数据。
- 网站的分享封面不会修改 YouTube 或 Bilibili 视频自身的封面。直接分享视频链接时，由视频平台提供预览信息。
- 必须将新增图片与网页一起提交、推送，待 GitHub Pages 部署完成后分享设置才会生效。平台可能缓存旧预览，实际显示仍由平台决定。

已有 PNG 可直接发布；只有重新排版分享封面时才需要在 Windows PowerShell 中运行 `scripts/build_social_previews.ps1`，无需安装额外依赖。
