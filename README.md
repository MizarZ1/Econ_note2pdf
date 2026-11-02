# Econ_note2pdf

将高级经济学板书照片与手写笔记 PDF 整理为可直接阅读、复习的 LaTeX 讲义和 PDF。识别与学科理解使用当前 agent 的宿主模型，本地脚本负责图片准备、来源管理、编译和交付。

## 项目状态

P1–P5 首版核心开发完成，本地处理、LaTeX/PDF 交付、宿主入口与安装包已提供。当前为 v0.1 预览版；已增加一个经授权的真实板书中文排版案例，完整课程和跨宿主验收尚未完成。

## 首版能力

- 优先处理板书照片，同时支持手写笔记 PDF。
- 面向宏观、微观、计量与经济数理，覆盖公式、推导、图与表格。
- 在 Codex、Claude Code 等 agent 宿主中使用宿主模型完成识别与整理。
- 支持忠实转录、复习讲义或两种版本；交付 PDF 和可编辑 LaTeX 工程。
- 正文强调逻辑、完整性与可读性；一般复核事项放入附录，技术日志保留在工程目录。
- 保留原件、高清分块和裁切来源，支持断点恢复、过期状态识别与失败单元隔离。
- 无独立模型 API、OCR 服务或 API key 依赖；无需多 agent 并行。

完整真实材料测试和用户验收另行安排。

## 安装

需要 Node.js/npm 才能使用 Skills CLI；从 GitHub 直接安装到 Codex 的个人 skill 目录：

```sh
npx skills add https://github.com/MizarZ1/Econ_note2pdf/tree/main/advanced-econ-note2pdf --agent codex --global
```

仓库私有期间需具备 Git 访问权限；公开分发前请按 [发布说明](docs/releasing.md) 生成不含开发历史的快照。安装后重新加载技能列表或开启新会话，再按下方环境说明安装本地依赖。

更新和卸载可用 `npx skills update`、`npx skills remove advanced-econ-note2pdf --agent codex --global`；也可用 ZIP 目录覆盖更新（先备份自定义改动）。安装只复制规则和脚本，不安装 TeX/Poppler 或配置模型。

## 使用

本仓库已经配置两种项目入口，共用 [skill 核心](advanced-econ-note2pdf/SKILL.md)：

| 宿主 | 项目入口 | 调用示例 |
| --- | --- | --- |
| Codex | `.agents/skills/advanced-econ-note2pdf` | `$advanced-econ-note2pdf 将这些板书整理成复习讲义` |
| Claude Code | `.claude/skills/advanced-econ-note2pdf` | `/advanced-econ-note2pdf 将这些板书整理成复习讲义` |
| DSH / 其他 agent | 显式读取完整 skill 目录内的 SKILL.md | 按文件中的流程，使用宿主视觉和本地工具 |

在此仓库启动宿主，提供材料路径与课程信息即可。宿主按需询问整理模式，然后查看图片、填写内容记录、编译和复核。不必手动逐条执行 CLI；CLI 本身不会识别板书。

独立安装可运行 `python3 tools/package_skill.py`，得到 `dist/advanced-econ-note2pdf-v0.1.zip` 与 SHA-256 校验文件。将 ZIP 中的完整文件夹解压到宿主支持的 skill 目录；平台不支持符号链接时直接复制完整目录。具体加载约定与验证状态见 [宿主说明](advanced-econ-note2pdf/references/hosts.md)。

## 环境

Python 3.9+、Pillow、pypdf；PDF 渲染需要 Poppler，编译需要 XeLaTeX、latexmk 及包含 ctex/Fandol、TikZ/PGFPlots 等包的 TeX 发行版。HEIC 可选 pillow-heif 或 macOS sips。

先诊断本机能力：

```sh
python3 advanced-econ-note2pdf/scripts/econ_note.py doctor
```

需要安装 Python 包时建议使用虚拟环境：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r advanced-econ-note2pdf/requirements.txt
```

之后让宿主使用该虚拟环境的 Python 运行脚本。doctor 会分别显示图片、PDF 导入、编译和预览能力，脚本不自动修改系统环境。

## 交付与恢复

工作项目放在 `work/` 等独立目录。最终交付位于该项目的 `output/`：每种模式有 PDF、可编辑工程 ZIP 和交付状态 JSON。ZIP 包含实际使用的裁切素材及来源记录，不默认包含全部原件或技术日志。

修改原图处理方式、正文、课程宏或素材后，旧复核/构建会失效；恢复先查询 status。默认打包要求当前内容与页面均完成复核，显式提前打包会标为 unreviewed，缺失内容则标为 partial。

## 开发与验证

合成工程自检已经覆盖中文、数学、图表、引用、附录、编译错误隔离、打包限制和独立工程重编译。Codex 的项目技能发现已实际验证；Claude Code 的加载配置已提供，DSH 专用加载接口待核实。

已用一张真实数理经济学板书完成中文讲解、公式转录、编译和逐页查看；此案例不代表整套课程或跨宿主效果已验收。

```sh
python3 tools/check_repo.py
python3 tools/dev_check.py                 # 无需 TeX 的合成文件链路
python3 tools/dev_check.py --with-latex    # 本地完整编译、渲染与恢复自检
python3 tools/package_skill.py
```

GitHub Actions 运行结构检查、合成文件链路和安装包构建；完整 TeX 自检在开发机执行。开发者先阅读 [AGENTS.md](AGENTS.md)，再按 [五阶段执行计划](docs/plans/2026-10-31-v0.1-development-plan.md) 工作；实现说明见 [开发文档](docs/development.md)，数据结构见 [内容契约](advanced-econ-note2pdf/references/content-model.md)。

## 数据与许可

Python 脚本不调用模型 API。图片识别由当前宿主执行，图片是否发往云端、保存多久及模型费用取决于宿主配置；全流程不保证离线。分享 PDF/工程前检查正文、附录与实际引用裁切中的私人信息。工程来源记录不导出原文件名、其他模式内容或内部事项详情；完整记录留在本地工作目录。

编译禁用 latexmk 自动 RC、shell escape，设置 TeX 的 paranoid 读写选项，并在组装前拒绝片段中的常见文件操作、动态命令构造和外部图片路径。它不是操作系统沙箱：不应在有敏感数据的环境运行陌生 TeX 工程；需要处理不可信工程时另用隔离容器。不要为绕过错误放宽读写设置。中文使用 ctex/Fandol；以当前编译日志和全部渲染页确认中文字形。

代码、skill 规则、文档与自有模板采用 [MIT](LICENSE)；许可证不授予用户输入材料或生成讲义中第三方内容的权利。贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题见 [SECURITY.md](SECURITY.md)，版本变化见 [CHANGELOG.md](CHANGELOG.md)。
