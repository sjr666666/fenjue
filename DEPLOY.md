# 部署说明

站点是纯静态页，GitHub Pages 直接从本目录的 `main` 分支发布。

## 目录里有什么

| 文件 | 作用 |
|---|---|
| `*.md` | 内容正文，站点运行时抓取并渲染 |
| `index.template.html` | 页面模板（样式 / 脚本 / 版式都在这里） |
| `marked.min.js` | Markdown 解析器，构建时内联进 `index.html` |
| `index.html` | **构建产物**，由下面两条命令生成，不手改 |
| `mermaid.min.js` | 图表渲染库，按需加载（只有含图的文档才会下载） |
| `sanitize.py` | 脱敏工具，推送前必须校验通过 |
| `build.py` | 把模板与 marked 合成单文件 `index.html` |
| `03-我的拷打树.html` | 独立交互版页，不参与构建 |
| `manifest.webmanifest` / `icon*` | 添加到主屏幕（PWA）所需资源 |

## 改内容的流程

```powershell
# 1. 编辑 *.md 或 index.template.html
# 2. 改了模板就重新构建
python build.py
# 3. 推送前校验脱敏（必须有输出“校验通过”）
python sanitize.py --check
# 4. 提交
git add -A; git commit -m "update"; git push
```

## 脱敏

敏感词表放在 `.sanitize-map.txt`（已被 `.gitignore` 排除，不会进公开仓库）。
本目录里的 `*.md` 是**脱敏后的发布版**；含真名 / 学校 / 真实公司名的工作稿请留在本机，
不要直接拷进来。

## 手机 / 平板

页面按手机 / 平板做了适配，实测结论见 `_work` 之外无需额外配置：

- 手机（360 / 375 / 393）：单列卡片，正文 15px，触控热区 ≥ 40px
- 折叠屏 / 小平板（673 / 768）：基准字号 16px，卡片双列
- 大屏平板（≥ 1000px）：目录改为右侧抽屉，正文上限 840px
- 含 Mermaid 图的文档：图可左右滑动，或点“放大查看”进入可缩放全屏视图
- 站点为 PWA，可“添加到主屏幕”后全屏阅读，支持深色模式
