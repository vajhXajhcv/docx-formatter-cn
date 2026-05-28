# 使用示例

## 自定义模板

通过 JSON 文件自定义排版参数：

```bash
python -m docx_formatter.cli convert input.md -o output.docx --template-file custom_template.json
```

可用的配置字段参见 `custom_template.json` 示例。

## 公式丰富的论文

```markdown
# 基于深度强化学习的机器人控制

## 摘要

本文研究了...

## 一、引言

强化学习通过智能体与环境的交互学习最优策略[1]。

价值函数定义为：

$$V^{\pi}(s) = \mathbb{E}_{\pi}\left[\sum_{t=0}^{\infty} \gamma^t r_{t+1} \mid s_0 = s\right]$$

Q-learning 更新规则：

$$Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[r_{t+1} + \gamma \max_a Q(s_{t+1}, a) - Q(s_t, a_t)\right]$$

策略梯度定理：

$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot Q^{\pi_\theta}(s,a)\right]$$

## 二、方法

### 2.1 网络架构

| 层 | 维度 | 激活函数 |
|----|------|---------|
| 输入 | $84 \times 84 \times 4$ | - |
| 卷积 | $20 \times 20 \times 32$ | ReLU |
| 全连接 | 512 | ReLU |
| 输出 | $|A|$ | - |

### 2.2 训练过程

损失函数：

$$\mathcal{L}(\theta) = \mathbb{E}_{(s,a,r,s') \sim D}\left[\left(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta)\right)^2\right]$$

## 参考文献

[1] Mnih V, et al. Human-level control through deep reinforcement learning[J]. Nature, 2015.
```
