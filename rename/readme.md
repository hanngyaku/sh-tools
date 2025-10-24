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