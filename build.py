#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 index.template.html + marked.min.js 合成为可部署的 index.html。

流程：build.py（合成单文件 site） -> sanitize.py（发布前脱敏校验）
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TPL = ROOT / "index.template.html"
LIB = ROOT / "marked.min.js"
OUT = ROOT / "index.html"
PLACEHOLDER = "__MARKED_LIB__"


def main() -> int:
    for p in (TPL, LIB):
        if not p.exists():
            sys.exit(f"缺少文件：{p}")
    tpl = TPL.read_text(encoding="utf-8")
    if tpl.count(PLACEHOLDER) != 1:
        sys.exit(f"模板中 {PLACEHOLDER} 出现 {tpl.count(PLACEHOLDER)} 次，应为 1 次")
    lib = LIB.read_text(encoding="utf-8").strip()
    if "</script" in lib.lower():
        sys.exit("marked.min.js 含 </script，不能内联")
    out = tpl.replace(PLACEHOLDER, lib)
    OUT.write_text(out, encoding="utf-8", newline="")
    print(f"已生成 {OUT.name}：{len(out):,} 字节（模板 {len(tpl):,} + marked {len(lib):,}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
