# scripts/ — 已验证的 GDUT 论文 docx 构建管线参考实现

源自 2026-10《智能配电网光储协同的电压治理系统方案设计》课程报告项目（LibreOffice 渲染 + 程序化校验 + 视觉抽查全部通过）。**新文档 = 复制本目录到工作区 → 改以下参数 → 跑管线**。

## 文件角色

| 文件 | 角色 | 新文档需改动处 |
|---|---|---|
| `build_report.py` | 通用构建库：setup_styles/setup_sections（页面边距、页码分节）、set_run_fonts（中西文字体）、heading（H1 另起一页）、body_para（1.5 倍行距+首行缩进2字符）、add_formula（OMML 公式居中+编号右对齐）、three_line_table（三线表+表头重复+行不拆分）、add_figure、page_break、OMML 构造器（frac/ssub/ssup/rad/dparen/omath） | 顶部 `WORK/OUTDIR/FIGS/DOC_PATH` 路径；`FORMULAS` 字典按新文档公式重写（key 即编号，如 '2.1'） |
| `report_content.py` | 内容模块范例：`CH1..CH6` 章节块列表（'h2'/'p'/'f'/'fig'/'tableN' 元组）、行内标记（`**粗体**`、`[[n]]`上标引用、`_{}``^{}`上下标）、REFS 文献表、TABLE* 表格数据、build_cover/build_front_matter（封面信息表/摘要/静态目录）、emit_chapter、build(toc_entries) | 全部内容；章节元组结构保持不变即可直接驱动 emit_chapter |
| `finalize_report.py` | 目录页码迭代收敛：build→soffice 渲染→PDF 提取各标题实际页码→回填目录重build，循环至页码稳定；用点线引导符识别目录页避免误匹配 | 无需大改（其从 render_pdf 读标题表） |
| `render_pdf.py` | soffice→PDF→逐页 PNG（pymupdf dpi=110）+ 标题所在页提取 | `HEADINGS_L1/HEADINGS_L2` 改为新文档标题（含全角空格，如 '1　绪论'） |
| `verify_docx.py` | 校验：OMML 公式数、嵌入图片数、上标引用与文献表双向覆盖、加粗结论数、图表题清单 | `DOCX` 路径；`n_math == N` 预期公式数 |

## 标准执行序列（工作区内）

```
del toc_data.json
python finalize_report.py     # 迭代收敛，输出目录页码
python verify_docx.py         # 结构校验
python render_pdf.py          # 渲染逐页 PNG 供视觉抽查
```

## 本机环境要点

- LibreOffice：`render_pdf.py` 自动探测 PATH / `C:\Program Files\LibreOffice` 中的 soffice；便携版用户把路径加入 `_CAND` 列表
- Windows/cmd：`python -c` 含引号或中文会**静默失败**，一律写 .py 文件执行；无 tail/head/heredoc。
- Word 口径字数 = 汉字数 + 西文/数字串数，统计脚本自写（参考 SKILL.md 第 10 节）。
- 渲染后若行距异常偏高：检查 sectPr 中的 docGrid 并删除；不要用 exact 行距（LibreOffice 忽略）。
