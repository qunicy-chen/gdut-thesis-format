# gdut-thesis-format

广东工业大学（GDUT）本科生**毕业设计/课程报告 Word 格式**的 [ZCode](https://zcode.ai) 技能（skill）。装好后，AI 助手在帮你写论文时会自动按广工规范排版：三线表、OMML 原生公式、GB/T 7714 参考文献、目录页码自动回填，并附带一整套经过实际项目验证的 python-docx 构建/校验脚本。

## 功能

- 按学校规范排版：A4 页面与页边距、章/节标题黑体分级、正文小四宋体 1.5 倍行距、页脚页码从正文起编
- **三线表**（1.5pt 顶底线 + 0.75pt 栏目线）、表题表上/图题图下
- **公式为 Word 原生"插入公式"对象**（OMML），居中 + （章.序）编号右对齐，非图片/文本
- **GB/T 7714-2015** 顺序编码制参考文献，正文 `[n]` 上标引用，脚本自动校验引用与文献表双向覆盖
- **目录页码迭代回填**：构建 → LibreOffice 渲染 → 提取真实页码 → 重写目录，直至收敛
- 按 **Word 字数口径**（汉字 + 西文串）统计字数，避免"写了多少字"的统计偏差

## 安装

**方式 A：git（可随时 `git pull` 更新）**

```
git clone https://github.com/<仓库地址>/gdut-thesis-format C:\Users\<你的用户名>\.agents\skills\gdut-thesis-format
```

macOS / Linux：

```
git clone https://github.com/<仓库地址>/gdut-thesis-format ~/.agents/skills/gdut-thesis-format
```

**方式 B：直接下载 ZIP（无需 git）**

1. 点击仓库页面绿色 **Code** 按钮 → **Download ZIP**
2. 解压后，把 `gdut-thesis-format` 文件夹整个放到你的用户目录下：
   - Windows：`C:\Users\<你的用户名>\.agents\skills\gdut-thesis-format\`
   - macOS / Linux：`~/.agents/skills/gdut-thesis-format/`
3. 确保 `SKILL.md` 直接位于该文件夹内

安装后重启 ZCode 即可被发现。

## 依赖

- Python 3.10+，安装库：`pip install python-docx matplotlib pymupdf pillow`
- LibreOffice（可选）：用于渲染校验与目录页码回填；未安装时仍可生成 docx，仅缺少渲染检查步骤

## 使用

对 AI 助手直接说需求即可自动触发，例如：

> 帮我写一份广工格式的课程报告，题目《……》

或显式调用：`/gdut-thesis-format`。

## 目录结构

```
gdut-thesis-format/
├── SKILL.md                 # 技能说明（给 AI 看的触发与工作流）
├── references/format-spec.md # 完整格式规范细则
└── scripts/                  # 已验证的构建管线（用法见 scripts/README.md）
```

## 说明

- 格式细则依据《广东工业大学本科生毕业设计（论文）格式规范》整理；学校发布新版规范时，请以官方文件为准。
- `scripts/` 中的脚本源自一次真实课程报告项目（23 页、OMML 公式、20 篇文献全流程校验通过），使用前按 `scripts/README.md` 修改顶部路径常量。

## License

MIT
