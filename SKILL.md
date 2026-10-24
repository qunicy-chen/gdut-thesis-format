---
name: gdut-thesis-format
description: 广东工业大学（GDUT）本科生毕业设计与课程报告的 Word 文档格式规范与完整排版实现。Use whenever the user asks to write, format, check, or render a 论文/毕业设计/课程报告/开题报告 docx for 广东工业大学/GDUT/广工, or any Chinese academic docx needing GDUT thesis format (三线表、OMML 原生公式、GB/T 7714 引用、目录页码回填、Word 字数口径). Includes proven python-docx build pipeline, LibreOffice render-verify loop, and reusable scripts.
---

# GDUT 论文格式技能

为广东工业大学本科生论文/课程报告生成**格式合规**的 Word（.docx）文档。规范来源：学校统一发布的《广东工业大学本科生毕业设计（论文）格式规范》（用户机器上有原文 PDF，位于 `C:\Users\C2422\Desktop\文件集合\学习\课程设计与作业\智能电网\` 下；若找不到则以本技能 `references/format-spec.md` 为准）。

**先读 `references/format-spec.md`**（完整格式细则），排版时**直接复用 `scripts/` 下已验证的脚本**（不要从零重写）。

## 核心工作流

1. **内容规划**：确定章节结构（绪论→…→总结展望→参考文献；课程报告通常无附录要求）。
2. **插图**：matplotlib 生成 300 dpi PNG（`plt.rcParams['font.family']='SimHei'`，`axes.unicode_minus=False`）；架构/流程图注意框内文字与标题行间距（正文块放 y+h*0.44 以下，行数多时用 bf 参数下移）。
3. **构建 docx**：以 `scripts/report_content.py` 为模板写内容模块（`CH1..CHn` 块列表 + `emit_chapter`），调用 `scripts/build_report.py` 的工具函数。内联标记语法：`**加粗**`、`[[n]]`→上标引用、`_{下标}`、`^{上标}`。
4. **目录页码回填**：运行 `scripts/finalize_report.py`（迭代：构建→LibreOffice 渲染→提取各标题实际页码→重写目录→直至收敛）。首次运行前 `del toc_data.json`。
5. **程序化校验**：`scripts/verify_docx.py` 检查公式数/图片数/引用覆盖/文献数；`scripts/word_count.py` 按 **Word 字数口径**（汉字 1 + 西文单词/数字串各 1）统计字数——用户问"多少字"时必须用此口径，纯汉字数会明显偏低。
6. **渲染抽查**：`scripts/render_pdf.py` 输出逐页 PNG，视觉检查公式分式/上下标、三线表、图题居中、目录点线。

## 格式速查（详见 references/format-spec.md）

| 元素 | 规范 |
|---|---|
| 页面 | A4；边距上 30 / 下 25 / 左 30 / 右 20 mm |
| 章标题 | 三号黑体加粗居中，**每章另起一页**；标题≤15 字不用标点 |
| 节/条标题 | 节小四黑体加粗；条小四黑体；节、条段前段后各 0.5 行 |
| 正文 | 小四宋体（数字字母 TNR），1.5 倍行距，首行缩进 2 字符 |
| 页码 | 小五 TNR，页脚右侧，**从绪论连续编至附录**；封面/摘要/目录不编 |
| 表 | 表题**表上**居中五号黑体加粗；三线表（顶/底 1.5pt、表头下 0.75pt，**无竖线**）；表内五号宋体；表头跨页不拆 |
| 图 | 图题**图下**五号宋体；分图号 (a)(b) 置于分图之下；图注小五宋体置图题之上 |
| 公式 | 居中，编号（章.序）右对齐、不加虚线；长公式在＝处转行（tab stops：Cm(7.9) 居中 + Cm(15.9) 右对齐） |
| 引用 | GB/T 7714-2015 顺序编码制；正文 `[n]` **上标**（小四号）；行文说明时排齐不上标；不得置于标题处 |
| 文献表 | 标题居中三号黑体加粗；条目**小四宋体**、序号左顶格、末以"．"结束 |
| 摘要/关键词 | "摘要"三号黑体加粗；正文小四宋体；下空一行"关键词"**四号黑体加粗**；3~5 个，**逗号分隔、末尾无标点**；英文摘要另起页，"Abstract"三号 TNR 加粗、"Key words:"四号 TNR 加粗 |
| 目录 | 三级标题（1/1.1/1.1.1）；**一级条目小四黑体、其余小四宋体**；页码点线右对齐，须与正文一致 |
| 毕业设计封面 | 题目二号黑体加粗居中；学院/专业/年级班别/学号/姓名/指导教师三号黑体加粗；另含书脊规范（见 format-spec §10） |
| 章节顺序 | 正文→结论→参考文献→致谢→附录（附录图表式单独编序：图A1/式(B3)） |

## 关键坑（均为实战验证，勿重蹈）

1. **公式必须是 OMML**（`<m:oMath>`，即 Word"插入→公式"），绝不能是图片或纯文本——用户会专门检查。用 build_report.py 的 `frac/ssub/ssup/rad/dparen/omath` 构造器。
2. **中文与西文字体要分别设置**：python-docx 需写 `w:rFonts` 的 `w:eastAsia`（宋体/黑体）+ `w:ascii`（TNR），只设 `font.name` 不够。
3. **首行缩进**用 `firstLineChars=200`（字符单位）而非固定磅值，跨字号稳定。
4. **LibreOffice 渲染怪癖**：sectPr 里的 docGrid 会撑高行距（构建后要 strip）；`lineRule=exact` 被忽略（别用它压行距）；静态目录段落比 TOC 域渲染更一致；宋体 12pt 自然行高≈17.7pt，1.5 倍行距≈26.5pt/行**是正确的**，不要误判为行距过大。
5. **目录回填**要在渲染 PDF 里用"点线引导符（.....）"识别目录页本身，避免把目录页上的标题文本当成正文标题匹配。
6. **三线表**用表格边框 XML 实现（顶/底 sz=12 即 1.5pt、表头下 sz=6 即 0.75pt，其余边框 none），并设 `tblHeader`（跨页重复表头）+ `cantSplit`（行不跨页拆分）。
7. **本机环境**（Windows/cmd）：`python -c` 带引号或中文参数会**静默失败**——一律写 .py 脚本文件再运行；heredoc 不可用；LibreOffice 便携版在 `C:\Users\C2422\LO_portable\program\soffice.exe`，需加 `-env:UserInstallation=file:///C:/Users/C2422/LO_profile`。
8. **交付前自检**：OMML 数、图片数、上标引用覆盖（每个文献号至少被引一次、无越界号）、图表题编号连续、目录单页且页码与实际一致。

## scripts/ 目录（已验证的参考实现）

源自 2026-10《智能配电网光储协同的电压治理系统方案设计》课程报告项目（格式校验通过）。用法见 `scripts/README.md`：

- `build_report.py` — 通用构建库：样式/字体/标题/正文/三线表/OMML 公式/插图/页码分节
- `report_content.py` — 内容模块范例（章节块列表 + 行内标记语法 + 文档组装）
- `finalize_report.py` — 目录页码迭代收敛循环
- `render_pdf.py` — soffice→PDF→逐页 PNG + 标题页码提取（`HEADINGS_L1/L2` 需按新文档改）
- `verify_docx.py` — 程序化校验模板（预期公式数等需按新文档改）

## 常见变体

- **课程报告**：封面用"课程名+报告"抬头（信息表下划线式）；字数要求常为"3000 字以上"（按 Word 口径，留 30–50% 余量即可，勿写至上万）。
- **毕业设计**：封面/书脊按 format-spec §10（题目二号黑体、字段三号黑体）；另含开题报告、外文翻译（20000 印刷字符或 5000 汉字）、致谢、附录；分类型字数/文献量要求见 format-spec §12（如工程类≥15000 字、文献≥10 且外文≥2）。
- 文献数量要求注意听清口径：课程报告常见"总数≥20 且**英文文献≥5**"；毕业设计按类型表执行——以用户当时的说法为准。
