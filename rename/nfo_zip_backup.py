#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="备份指定目录下的 .nfo 文件到 zip（保留相对目录结构）。"
    )
    parser.add_argument("source_dir", help="源目录路径，例如 /mnt/xxx/xxx")
    return parser


def collect_nfo_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in source_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() == ".nfo":
            files.append(path)
    return sorted(files)


def create_zip_path(source_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return source_dir / f"nfo_backup_{timestamp}.zip"


def run(source_dir_arg: str) -> int:
    source_dir = Path(source_dir_arg).expanduser().resolve()
    if not source_dir.exists():
        print(f"错误: 源路径不存在: {source_dir}", file=sys.stderr)
        return 2
    if not source_dir.is_dir():
        print(f"错误: 源路径不是目录: {source_dir}", file=sys.stderr)
        return 2

    start = time.time()
    zip_path = create_zip_path(source_dir)

    # 自动覆盖同名文件（同秒重复执行时可能出现同名）
    if zip_path.exists():
        zip_path.unlink()

    nfo_files = collect_nfo_files(source_dir)

    try:
        with ZipFile(zip_path, mode="w", compression=ZIP_DEFLATED) as zf:
            for file_path in nfo_files:
                arcname = file_path.relative_to(source_dir)
                zf.write(file_path, arcname=str(arcname))
    except OSError as exc:
        print(f"错误: 写入 zip 失败: {exc}", file=sys.stderr)
        return 1

    elapsed = time.time() - start
    print(f"备份完成: {zip_path}")
    print(f"文件数量: {len(nfo_files)}")
    print(f"耗时: {elapsed:.2f}s")
    if not nfo_files:
        print("提示: 未找到 .nfo 文件，已创建空 zip。")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run(args.source_dir)


if __name__ == "__main__":
    sys.exit(main())
