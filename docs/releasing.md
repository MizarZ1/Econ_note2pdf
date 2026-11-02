# 发布方式

当前仓库是私有开发库，其 Git 历史含个人提交身份。不要通过改一个当前文件或更改 Git 配置来声称历史已脱敏。保持开发历史，使用 `git archive HEAD` 在临时目录生成当前文件快照，经内容检查后创建独立的公开分发库；不复制 `.git`、私人材料、`.local`、工作目录或本地日志。不强推或重写现有共享历史。

公开分发库需要保留根 LICENSE、skill/LICENSE、README、安装说明和有效资源。更新 README 中安装 URL 为实际分发仓库。维护者发布时填写 GitHub Description 与 Topics（economics、latex、agent-skills），启用私密漏洞报告。

发布前运行结构检查、工程链路、publication_check，检查 `git diff --check`。执行 `python3 tools/package_skill.py`；检查 ZIP 文件列表、LICENSE 与 SHA-256。首次可建立 v0.1.0-preview 标签和预览 Release，附安装包与校验文件；创建公开仓库、改可见性和发布 Release 需明确发布指令。

源照片、生成讲义不随公开 Release 发布，除非另外取得具体授权。
