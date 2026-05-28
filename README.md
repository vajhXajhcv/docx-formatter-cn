# docx-formatter-cn

> 中文 Word 文档智能排版工具 —— 融合 Lark-Formatter 的 Pipeline 引擎与 docx-skill-4-cn-paper 的学术排版方案

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 功能特性

| 特性 | 说明 |
|------|------|
| 📝 **Markdown → Word** | 一键将 Markdown 转为符合中文学术规范的 `.docx` |
| ➗ **LaTeX 公式** | LaTeX → Word 原生 OMML 公式（可编辑，非图片） |
| 📊 **三线表** | 自动生成标准学术三线表 |
| 🔤 **中文字体** | 宋体/黑体 + Cambria Math，中英文混排优化 |
| 🔢 **自动编号** | 标题、图表、公式自动编号 |
| 📑 **目录生成** | 自动插入可更新的 Word 目录域 |
| 📚 **上标引用** | `[n]` 格式自动转为上标引用 |
| 🎨 **多模板** | 课程论文、毕业论文、数学建模、公文等预设模板 |
| 🤖 **AI Skill** | 可作为 AI Agent Skill 调用 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/vajhXajhcv/docx-formatter-cn.git
cd docx-formatter-cn

# 安装依赖
pip install -r requirements.txt

# 或安装为包
pip install -e .
```

要求：Python 3.10+

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

### AI Skill 调用

```bash
# Node.js wrapper
node skill/scripts/new_doc.js input.md output.docx 课程论文
```

## Markdown 语法支持

```markdown
# 一级标题
## 二级标题
### 三级标题

正文段落，支持**粗体**和*斜体*。

行内公式：$E = mc^2$

块级公式（自动编号）：
$$Q_n(x, a) = (1 - \alpha_n) Q_{n-1}(x, a) + \alpha_n [r_n + \gamma V_{n-1}(y_n)]$$

引用上标：本文提出了改进方案[1][2]。

| 符号 | 说明 |
|------|------|
| $S$ | 状态空间 |
| $A$ | 动作空间 |

![图1](images/fig1.png)

---

## 参考文献

[1] 作者. 标题[J]. 期刊, 2024.
```

## 模板预设

| 模板 | 适用场景 | 页面 | 行距 | 正文字号 |
|------|---------|------|------|---------|
| `课程论文` | 高校课程论文、毕业设计 | A4, 2.5cm 边距 | 1.5倍 | 小四(12pt) |
| `毕业论文` | 学位论文 | A4, 3.0/2.5cm 边距 | 1.5倍 | 小四(12pt) |
| `数学建模` | 数学建模竞赛 | A4, 2.0cm 边距 | 单倍 | 小四(12pt) |
| `公文` | 政府/企业公文 | A4, 标准边距 | 1.5倍 | 三号(16pt) |

## 公式支持

基于自研 `latex2mathml → MathML → OMML` 引擎，常用 LaTeX 均可转换：

| LaTeX | 效果 |
|-------|------|
| `x^2`, `a_n` | 上标/下标 |
| `\frac{a}{b}` | 分数 |
| `\sqrt{x}`, `\sqrt[n]{x}` | 平方根/n次根 |
| `\sum_{i=1}^{n}`, `\int_{0}^{\infty}` | 求和/积分 |
| `\alpha`, `\beta`, `\gamma` | 希腊字母 |
| `\begin{matrix} ... \end{matrix}` | 矩阵 |

## 项目架构

```
docx-formatter-cn/
├── src/docx_formatter/
│   ├── converter/          # Markdown 解析 + docx 构建
│   │   ├── markdown_parser.py
│   │   ├── docx_builder.py
│   │   └── toc.py          # 目录域生成
│   ├── formula/            # LaTeX → MathML → OMML 公式引擎
│   │   └── mathml_to_omml.py
│   ├── templates/          # 模板预设（预留）
│   ├── cli.py              # 命令行入口
│   └── config.py           # 配置系统
├── skill/
│   ├── SKILL.md            # AI Skill 使用文档
│   └── scripts/
│       └── new_doc.js      # Node.js 封装
├── tests/                  # 测试样例
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 技术实现

### 公式引擎

与 docx-skill-4-cn-paper 不同，本项目采用**纯 Python 方案**：

1. `latex2mathml` 将 LaTeX 转为 MathML
2. 自研 `mathml_to_omml.py` 将 MathML 映射为 Word OMML XML
3. 通过 `python-docx` 底层 `lxml` 直接插入 `<m:oMath>` 元素

优势：无需 Node.js 子进程，Python 核心自给自足，跨平台更稳定。

### 与上游项目的关系

| 本项目模块 | 来源项目 | 继承/改进 |
|-----------|---------|----------|
| Pipeline 引擎设计 | [Lark-Formatter](https://github.com/Alouetter/Lark-Formatter) | 提取核心思想，重写轻量版 |
| Markdown 解析 | Lark-Formatter | 继承并增强（公式、三线表） |
| 场景配置系统 | Lark-Formatter | 大幅简化，YAML/JSON 模板预设 |
| LaTeX→Word 公式 | [docx-skill-4-cn-paper](https://github.com/Gostyan/docx-skill-4-cn-paper) | 移植 `mathml-to-docx.js` 到 Python |
| 中文学术排版 | docx-skill-4-cn-paper | 吸收字体/三线表/编号/引用方案 |
| AI Skill 形态 | docx-skill-4-cn-paper | 保留 Node.js 封装层，底层调用 Python |

## 开发计划

- [x] 核心公式引擎（MathML → OMML）
- [x] Markdown → docx 转换器
- [x] 三线表、字体、页眉页脚
- [x] 模板系统（课程论文/毕业论文/数学建模/公文）
- [x] CLI 命令行工具
- [x] AI Skill 封装
- [x] 目录域生成
- [ ] PySide6 GUI（可选）
- [ ] 现有 docx 格式修正（Pipeline 规则引擎）
- [ ] 更多 LaTeX 公式支持（矩阵、分段函数等）

## 开源协议

MIT License — 详见 [LICENSE](LICENSE)

## 致谢

- [Lark-Formatter](https://github.com/Alouetter/Lark-Formatter) — 毕业论文排版引擎
- [docx-skill-4-cn-paper](https://github.com/Gostyan/docx-skill-4-cn-paper) — 中文学术 docx Skill
