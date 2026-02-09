## 🧩 backup.sh 使用方法

给脚本添加执行权限：

`chmod +x backup.sh`


运行备份：

`./backup.sh backup /Users/you/Movies /Users/you/NFOBackup`


运行还原：

`./backup.sh restore /Users/you/Movies /Users/you/NFOBackup`

💡 功能说明

find 命令递归查找 .nfo 文件。

cp -p 会保留修改时间等属性。

通过 ${file#$src_dir/} 提取相对路径并在目标中重建结构。

可安全重复执行，已存在的文件会被覆盖。

---

## 🧩 ZIP 版 NFO 备份与还原（Python）

### 1) 备份为 zip

```bash
python3 nfo_zip_backup.py /path/to/your/folder
```

- 会在源目录下生成：`nfo_backup_YYYYmmdd_HHMMSS.zip`
- ZIP 内仅包含 `.nfo/.NFO`，并保留相对目录结构

### 2) 直接用 unzip 还原到 zip 所在目录

```bash
unzip -o /path/to/your_backup.zip '*.nfo' '*.NFO' -d /path/to
```

- `-o`：覆盖已存在同名文件
- `-d /path/to`：恢复到 zip 所在目录

### 3) 用恢复脚本还原（推荐）

```bash
# 指定 zip
python3 nfo_zip_restore.py --zip ./nfo_backup_20260209_120000.zip

# 或在当前目录自动选择最新 nfo_backup_*.zip
python3 nfo_zip_restore.py --latest
```

- 默认还原到“zip 所在目录”
- 只还原 `.nfo/.NFO`
- 带路径安全检查（拒绝可疑路径）
