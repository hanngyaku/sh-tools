#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import re
import sys
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="从 nfo 备份 zip 中恢复 .nfo 到 zip 所在目录（覆盖同名文件）。"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--zip", dest="zip_path", help="指定要恢复的 zip 文件路径")
    group.add_argument(
        "--latest",
        action="store_true",
        help="在当前目录选择最新的 nfo_backup_*.zip 进行恢复",
    )
    return parser


def find_latest_zip(cwd: Path) -> Path | None:
    candidates = [p for p in cwd.glob("nfo_backup_*.zip") if p.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def is_suspicious_member(name: str) -> bool:
    if name.startswith(("/", "\\")):
        return True
    if re.match(r"^[A-Za-z]:", name):
        return True
    parts = PurePosixPath(name).parts
    return any(part == ".." for part in parts)


def validate_nfo_members(zip_path: Path) -> tuple[int, str | None]:
    try:
        with ZipFile(zip_path, "r") as zf:
            count = 0
            for info in zf.infolist():
                if info.is_dir():
                    continue
                if not info.filename.lower().endswith(".nfo"):
                    continue
                if is_suspicious_member(info.filename):
                    return 0, info.filename
                count += 1
            return count, None
    except BadZipFile:
        print(f"错误: 非法 zip 文件: {zip_path}", file=sys.stderr)
        raise


def restore_nfo_members(zip_path: Path, target_dir: Path) -> int:
    try:
        with ZipFile(zip_path, "r") as zf:
            restored = 0
            for info in zf.infolist():
                if info.is_dir() or not info.filename.lower().endswith(".nfo"):
                    continue
                # 二次保护，确保恢复阶段不会写出目标目录外。
                if is_suspicious_member(info.filename):
                    continue
                rel_path = PurePosixPath(info.filename)
                out_path = target_dir / Path(*rel_path.parts)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info, "r") as src, out_path.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                restored += 1
            return restored
    except OSError as exc:
        print(f"错误: 写入恢复文件失败: {exc}", file=sys.stderr)
        return -1


def resolve_zip_path(args: argparse.Namespace) -> Path | None:
    if args.latest:
        return find_latest_zip(Path.cwd())
    if args.zip_path:
        return Path(args.zip_path).expanduser().resolve()
    return None


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    zip_path = resolve_zip_path(args)
    if zip_path is None:
        print("错误: 当前目录没有找到 nfo_backup_*.zip", file=sys.stderr)
        return 2
    if not zip_path.exists() or not zip_path.is_file():
        print(f"错误: zip 文件不存在: {zip_path}", file=sys.stderr)
        return 2
    target_dir = zip_path.parent

    try:
        nfo_count, suspicious = validate_nfo_members(zip_path)
    except BadZipFile:
        return 1

    if suspicious:
        print(f"错误: 检测到可疑路径，已拒绝恢复: {suspicious}", file=sys.stderr)
        return 1

    if nfo_count == 0:
        print(f"提示: zip 内未找到 .nfo 文件: {zip_path}")
        return 0

    restored_count = restore_nfo_members(zip_path, target_dir)
    if restored_count < 0:
        return 1

    print(f"还原完成: {zip_path}")
    print(f"目标目录: {target_dir}")
    print(f"文件数量: {restored_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
