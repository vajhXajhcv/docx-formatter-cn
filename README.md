# docx-formatter-cn

> 中文 Word 文档智能排版工具 —— 融合 Lark-Formatter 的 Pipeline 引擎与 docx-skill-4-cn-paper 的学术排版方案

## 功能特性

- **Markdown → Word 一键转换**：将 Markdown 文件转换为符合中文学术规范的 `.docx`
- **LaTeX 公式 → Word 原生公式**：基于 `latex2mathml` + 自研 MathML→OMML 引擎，生成可编辑的 Word 原生公式
- **三线表自动生成**：标准学术三线表样式（顶线/栏目线/底线）
- **中文学术字体配置**：宋体/黑体 + Cambria Math，支持中英文混排
- **通用模板系统**：预设 课程论文、毕业论文、数学建模、公文 等模板
- **自动编号**：标题、图表、公式自动编号
- **上标引用**：`[n]` 格式自动转为上标引用
- **AI Skill 支持**：可作为 AI Agent Skill 调用

## 安装

```bash
pip install -r requirements.txt
```

依赖：Python 3.10+, python-docx, latex2mathml, lxml, PyYAML

## 快速开始

### 命令行

```bash
# Markdown 转 Word
python -m docx_formatter.cli convert input.md -o output.docx -t 课程论文

# 查看模板信息
python -m docx_formatter.cli info -t 毕业论文
```

### Python API

```python
from docx_formatter import convert_markdown_to_docx

with open("论文.md", "r", encoding="utf-8") as f:
    md_text = f.read()

convert_markdown_to_docx(md_text, "output.docx", template="课程论文")
```

### Markdown 语法支持

```markdown
# 一级标题
## 二级标题
### 三级标题

正文段落，支持**粗体**和*斜体*。

行内公式：$E = mc^2$

块级公式：
$$Q_n(x, a) = (1 - \alpha_n) Q_{n-1}(x, a) + \alpha_n [r_n + \gamma V_{n-1}(y_n)]$$

引用上标：本文提出了改进方案[1][2]。

| 符号 | 说明 |
|------|------|
| $S$ | 状态空间 |
| $A$ | 动作空间 |

![图1](images/fig1.png)
```

## 模板预设

| 模板 | 适用场景 | 特点 |
|------|---------|------|
| `课程论文` | 课程论文、毕业设计 | A4, 2.5cm 边距, 1.5倍行距, 小四 |
| `毕业论文` | 学位论文 | 更大边距, 标题字号分级更严格 |
| `数学建模` | 数学建模竞赛 | 紧凑边距, 单倍行距 |
| `公文` | 政府/企业公文 | 仿宋/方正小标宋, 16pt |

## 项目结构

```
docx-formatter-cn/
├── src/docx_formatter/
│   ├── converter/          # Markdown 解析 + docx 构建
│   ├── formula/            # LaTeX → MathML → OMML 公式引擎
│   ├── pipeline/           # 轻量排版 Pipeline（预留）
│   ├── templates/          # 模板预设
│   ├── cli.py              # 命令行入口
│   └── config.py           # 配置系统
├── skill/                  # AI Skill 封装
├── tests/                  # 测试
└── README.md
```

## 与上游项目的关系

- **Lark-Formatter** (https://github.com/Alouetter/Lark-Formatter): 提供 Pipeline 引擎设计思想、场景配置系统、Python-docx 排版经验
- **docx-skill-4-cn-paper** (https://github.com/Gostyan/docx-skill-4-cn-paper): 提供中文学术排版规范、公式处理方案（temml + mathmlToDocx）、三线表实现参考

## 开源协议

MIT License
