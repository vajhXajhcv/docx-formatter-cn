# Changelog

## [Unreleased]

### 新增

- **行内代码**：支持 Markdown 反引号 `` `code` `` 语法，渲染为等宽字体+浅灰背景
- **真正的超链接**：`[text](url)` 在 Word 中生成可点击的蓝色超链接（带 relationship）
- **模板导出 CLI**：新增 `export-template` 子命令，将预设模板导出为 JSON
- **批量转换**：`batch` 命令支持文件夹级 Markdown → docx 批量处理
- **图片尺寸控制**：`![alt](url =WxH)` 语法支持精确控制图片宽高
- **YAML Frontmatter**：自动提取 Markdown 文件顶部的 YAML 元数据（title/author/date/abstract/keywords），渲染为封面页
- **LaTeX 标准定界符**：支持 `\( ... \)` 行内公式和 `\[ ... \]` 块级公式

## [0.1.0] - 2026-05-28

### 新增

- **核心公式引擎**：自研 `mathml_to_omml.py`，将 LaTeX 通过 `latex2mathml` 转为 MathML，再映射为 Word 原生 OMML 公式
- **Markdown → docx 转换器**：支持标题、段落、列表、表格、代码块、图片、分页符
- **三线表自动生成**：标准学术三线表样式（顶线/栏目线/底线）
- **中文学术字体配置**：SimSun/SimHei + Cambria Math，支持中英文混排
- **自动编号**：标题、图表、公式自动编号
- **目录生成**：自动插入 Word TOC 域
- **上标引用**：`[n]` 格式自动转为上标引用
- **模板系统**：预设 课程论文、毕业论文、数学建模、公文 四种模板
- **自定义模板**：支持通过 JSON/YAML 文件加载自定义模板
- **CLI 命令行**：`convert`、`format`、`info` 三个子命令
- **现有 docx 修正模式**：对已有 Word 文档应用模板样式（页面/字体/段落/页眉页脚）
- **PySide6 GUI**：桌面应用，支持文件拖拽、模板选择、进度显示、双模式（生成/修正）
- **AI Skill 封装**：Node.js wrapper + SKILL.md 文档
- **引用块支持**：`> text` 渲染为带左边框的引用段落
- **任务列表支持**：`- [x]` / `- [ ]` 渲染为带复选框的列表项
- **下划线/删除线支持**：`<u>text</u>` / `~~text~~`
- **网络图片下载**：支持 `http/https` 图片 URL 自动下载插入
- **单元测试**：formula 和 markdown 解析器测试
- **CI 配置**：GitHub Actions 自动测试
