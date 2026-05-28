# docx-formatter-cn Skill

用于 AI Agent 将 Markdown 转换为符合中文学术规范的 Word 文档。

## 功能

- Markdown → `.docx` 一键转换
- LaTeX 公式 → Word 原生公式（可编辑）
- 三线表、自动编号、上标引用
- 多模板支持：课程论文、毕业论文、数学建模、公文

## 使用方法

### 方法 1：直接调用 Python CLI（推荐）

确保已安装依赖：
```bash
pip install python-docx latex2mathml lxml PyYAML
```

转换命令：
```bash
python -m docx_formatter.cli convert 论文.md -o 论文.docx -t 课程论文
```

### 方法 2：Python API

```python
import sys
sys.path.insert(0, "src")
from docx_formatter import convert_markdown_to_docx

md_text = """
# 论文标题

## 摘要

本文研究了...

## 一、引言

这是引言段落。

$$E = mc^2$$

## 参考文献

[1] 作者. 标题[J]. 期刊, 2024.
"""

convert_markdown_to_docx(md_text, "output.docx", template="课程论文")
```

## 支持的 Markdown 语法

- `# 标题` / `## 标题` / `### 标题`
- `**粗体**` / `*斜体*`
- `$行内公式$` / `$$块级公式$$`
- `| 表格 | 表格 |`
- `![图片](路径)`
- `[n]` 上标引用
- `---` 分页符
- ````代码块````

## 模板说明

| 模板名称 | 适用场景 |
|---------|---------|
| `课程论文` | 高校课程论文、毕业设计 |
| `毕业论文` | 学位论文 |
| `数学建模` | 数学建模竞赛 |
| `公文` | 政府/企业公文 |

## 公式支持

常用 LaTeX 公式均可转换：
- 上标/下标：`x^2`, `a_n`
- 分数：`\frac{a}{b}`
- 根号：`\sqrt{x}`, `\sqrt[n]{x}`
- 求和/积分：`\sum_{i=1}^{n}`, `\int_{0}^{\infty}`
- 希腊字母：`\alpha`, `\beta`, `\gamma`
- 矩阵：支持基本矩阵

## 注意事项

1. 图片路径相对于 Markdown 文件所在目录解析
2. 块级公式支持自动编号：`$$...\tag{1}$$` 或 `$$...(1)$$`
3. 生成的 docx 需在 Microsoft Word 或 WPS 中打开以获得最佳效果

## 项目地址

https://github.com/vajhXajhcv/docx-formatter-cn
