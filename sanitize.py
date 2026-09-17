#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fenjue 脱敏工具（发布目录内就地替换）。

敏感词表放在 .sanitize-map.txt（不进公开仓库），格式：
    真名[:=]替换文本
空行与 # 开头的行忽略。

用法：
    python sanitize.py            # 就地脱敏（幂等）
    python sanitize.py --check    # 只检查，命中敏感词则退出码 1
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAP_FILE = ROOT / ".sanitize-map.txt"
TARGET_GLOBS = ("*.md", "*.html", "*.webmanifest")


def load_map() -> list[tuple[str, str]]:
    if not MAP_FILE.exists():
        sys.exit(f"缺少脱敏词表：{MAP_FILE}")
    pairs: list[tuple[str, str]] = []
    for lineno, raw in enumerate(MAP_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            sys.exit(f"{MAP_FILE.name}:{lineno} 缺少 '='：{line}")
        key, _, val = line.partition("=")
        key = key.strip()
        if not key:
            sys.exit(f"{MAP_FILE.name}:{lineno} 左侧为空")
        pairs.append((key, val.strip()))
    # 长词优先，避免“靖安科技”先被“靖安”吃掉
    pairs.sort(key=lambda kv: len(kv[0]), reverse=True)
    return pairs


def targets() -> list[Path]:
    files: list[Path] = []
    for pattern in TARGET_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查，不修改文件")
    args = ap.parse_args()
    pairs = load_map()

    hits: list[str] = []
    changed: list[str] = []
    for path in targets():
        raw = path.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        found = [(k, v, text.count(k)) for k, v in pairs if k in text]
        if args.check:
            for k, _v, n in found:
                hits.append(f"{path.name}: 命中「{k}」x{n}")
            continue
        if not found:
            continue
        for k, v, _n in found:
            text = text.replace(k, v)
        path.write_text(("\ufeff" if bom else "") + text, encoding="utf-8", newline="")
        changed.append(f"{path.name}: " + ", ".join(f"{k}->{v}x{n}" for k, v, n in found))

    if args.check:
        if hits:
            print("脱敏校验未通过：")
            for h in hits:
                print("  " + h)
            return 1
        print(f"脱敏校验通过：{len(targets())} 个文件未发现敏感词。")
        return 0

    if changed:
        print("已完成脱敏：")
        for c in changed:
            print("  " + c)
    else:
        print("无需脱敏：未发现敏感词。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
