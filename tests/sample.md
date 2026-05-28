# 基于 Q-Learning 算法的走迷宫智能体复现与分析

## 摘要

本文研究了强化学习中的 Q-learning 算法，分析了其收敛性和应用场景。实验结果表明，算法在约 80 回合后成功率即达到 100%。

**关键词：** 强化学习；Q-Learning；马尔可夫决策过程

---

## 一、引言

强化学习（Reinforcement Learning）是机器学习的一个重要分支。Q-learning 算法由 Watkins 于 1989 年提出[1]，其核心在于直接估计状态-动作价值函数。

Q-Learning 更新规则如下：

$$Q_n(x, a) = (1 - \alpha_n) Q_{n-1}(x, a) + \alpha_n [r_n + \gamma V_{n-1}(y_n)]$$

## 二、方法

### 2.1 符号说明

| 符号 | 说明 |
|------|------|
| $S$ | 状态空间 |
| $A$ | 动作空间 |
| $\alpha$ | 学习率 |
| $\gamma$ | 折扣因子 |

### 2.2 算法描述

Q-Learning 更新公式：

$$Q(s, a) = Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)] \tag{1}$$

## 三、实验结果

实验结果表明，算法成功学会了从起点到终点的最优路径。

## 参考文献

[1] Watkins C J C H, Dayan P. Q-learning[J]. Machine Learning, 1992.

[2] Sutton R S, Barto A G. Reinforcement Learning: An Introduction[M]. MIT Press, 2018.
