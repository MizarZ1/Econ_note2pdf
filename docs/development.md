# 开发与自检

最低 Python 3.9。skill 的 `requirements.txt` 只声明 Pillow、pypdf；PDF 渲染另需本地 Poppler（`pdftoppm`），PDF 编译将在 P4 使用 XeLaTeX/latexmk。HEIC 可使用 `pillow-heif` 或 macOS `sips`；脚本不自动安装依赖。

```sh
python3 advanced-econ-note2pdf/scripts/econ_note.py doctor
python3 -m compileall -q advanced-econ-note2pdf/scripts
python3 tools/dev_check.py
```

`dev_check.py` 生成矩形与短文本的合成图片/PDF，检查文件导入、页面展开、分块、来源版本、裁切冲突与复核失效。它不调用模型、不含真实用户材料，不用于评价笔迹识别或讲义阅读质量。默认临时目录自动清理；`--keep .local/p3-check` 可保留产物定位问题。

## 已实现命令

```sh
python3 advanced-econ-note2pdf/scripts/econ_note.py init --project work/course --inputs /path/to/photo.jpg /path/to/notes.pdf --title '高级经济学' --mode both --domains macro
python3 advanced-econ-note2pdf/scripts/econ_note.py prepare --project work/course
python3 advanced-econ-note2pdf/scripts/econ_note.py crop --project work/course --source s0001 --box 0.1 0.2 0.8 0.9 --name phase-diagram
python3 advanced-econ-note2pdf/scripts/econ_note.py validate --project work/course
python3 advanced-econ-note2pdf/scripts/econ_note.py status --project work/course
```

初始化只生成待填写的逻辑单元；宿主查看 prepared 全图/分块后，根据 [内容契约](../advanced-econ-note2pdf/references/content-model.md) 写入 units 与 content。只有实际对照材料后才调用 `review --kind content --unit u001 --note '检查对象和结果'`。

多张照片组成一个单元时，可用 `unit` 新建单元，然后修改 `project.json.units` 的阅读顺序，移除已被替代的空单元 ID；磁盘上的旧文件保留。校验仍要求所有来源有覆盖记录，不能通过移除单元掩盖遗漏。

所有项目写操作使用锁；进程异常退出后先确认 `.econ-note.lock` 中 PID 已不再运行，再删除失效锁。每次更新 project.json 会在 history 保存旧版本；旧图像 revision 不覆盖。内容正文由宿主编辑，脚本不会重写。

## 开发记录

- P1：文档相对链接、JSON 示例解析与 diff 检查通过。
- P2：skill frontmatter/命名检查及参考链接检查通过。
- P3：开发自检结果将在该阶段完成后记录。真实材料测试、模型效果测试与用户验收仍未开展。
