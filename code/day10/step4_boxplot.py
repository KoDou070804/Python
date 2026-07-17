"""
Day 10 — 箱线图 (Box Plot)
内容：基本箱线图 · 多组对比 · 美化 · 叠加散点 · 综合练习
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False


# ============================================================
# 1. 最基本的箱线图
# ============================================================
# plt.boxplot() 只需要一组数据就能画

data = np.random.randn(100) * 10 + 50   # 50分左右，标准差10

plt.figure(1, figsize=(6, 4))
plt.boxplot(data)
plt.title("基本箱线图")
plt.ylabel("分数")
plt.grid(True, alpha=0.3)
plt.show()


# ============================================================
# 2. 看懂箱线图
# ============================================================
# 箱线图展示了5个统计量（从上到下）：
#   上边缘（最大值，不含异常值）
#   上四分位数 Q3（75% 的数据 ≤ 这个值）
#   中位数 Q2（50% 的数据 ≤ 这个值）
#   下四分位数 Q1（25% 的数据 ≤ 这个值）
#   下边缘（最小值，不含异常值）
#   ○ 圆圈 = 异常值（超出1.5倍IQR范围）

np.random.seed(42)
data = np.random.randn(200) * 10 + 50
# 手动加几个异常值
data = np.append(data, [95, 5, 98])

plt.figure(2, figsize=(6, 4))
box = plt.boxplot(data)

plt.title("箱线图各部分组成", fontsize=13)
plt.ylabel("数值")
plt.grid(True, alpha=0.3)

# 标注各部分的含义
q1 = np.percentile(data, 25)
q2 = np.percentile(data, 50)
q3 = np.percentile(data, 75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

plt.text(1.15, q3, f'  Q3 = {q3:.1f}', va='center', fontsize=10)
plt.text(1.15, q2, f'  中位数 = {q2:.1f}', va='center', fontsize=10)
plt.text(1.15, q1, f'  Q1 = {q1:.1f}', va='center', fontsize=10)
plt.text(1.15, upper, f'  上边缘 = {upper:.1f}', va='center', fontsize=10)
plt.text(1.15, lower, f'  下边缘 = {lower:.1f}', va='center', fontsize=10)

plt.show()

print(f"Q1={q1:.1f}, 中位数={q2:.1f}, Q3={q3:.1f}")
print(f"IQR={iqr:.1f}, 下边缘={lower:.1f}, 上边缘={upper:.1f}")
print(f"异常值: {data[(data < lower) | (data > upper)]}")


# ============================================================
# 3. 多组数据对比 — boxplot 最常用的场景
# ============================================================
np.random.seed(42)

# 模拟三个班级的成绩分布
class_a = np.random.normal(70, 12, 40)   # 均分70，标准差12
class_b = np.random.normal(75, 8, 40)    # 均分75，标准差8（班更整齐）
class_c = np.random.normal(65, 15, 40)   # 均分65，标准差15（两极分化）

plt.figure(3, figsize=(8, 5))
plt.boxplot([class_a, class_b, class_c], tick_labels=['A班', 'B班', 'C班'])
plt.title("三个班级成绩对比", fontsize=14)
plt.ylabel("分数")
plt.grid(True, alpha=0.3)
plt.show()

# 可以看到 B 班最整齐（箱子最矮），C 班最分散（箱子最高 + 异常值多）


# ============================================================
# 4. 箱线图的样式美化
# ============================================================
np.random.seed(42)
data = [np.random.normal(60 + i*5, 8, 50) for i in range(5)]

plt.figure(4, figsize=(10, 6))

boxes = plt.boxplot(data, tick_labels=['方法1', '方法2', '方法3', '方法4', '方法5'],
                     patch_artist=True,      # 填充颜色
                     notch=True,             # 凹口（显示中位数置信区间）
                     widths=0.5,             # 箱子宽度
                     showmeans=True,         # 显示均值
                     meanprops=dict(marker='D', markerfacecolor='red',
                                    markersize=6))

# 自定义每个箱子的颜色
colors = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'lightcoral']
for box, color in zip(boxes['boxes'], colors):
    box.set_facecolor(color)

plt.title("多组箱线图对比（带均值标记）", fontsize=14)
plt.ylabel("得分")
plt.grid(True, alpha=0.3)
plt.show()


# ============================================================
# 5. 箱线图 + 散点叠加（小提琴风格）
# ============================================================
# 箱线图看不到数据分布形状，所以常把原始数据点叠加上去

np.random.seed(42)
group_a = np.random.normal(70, 10, 30)
group_b = np.random.normal(80, 12, 30)
group_c = np.random.normal(65, 8, 30)

plt.figure(5, figsize=(8, 5))

# 先画箱线图（不显示异常值，因为我们能看到所有点）
bp = plt.boxplot([group_a, group_b, group_c],
                 tick_labels=['组A', '组B', '组C'],
                 patch_artist=True,
                 showfliers=False)  # 隐藏异常值标记

colors = ['#AED6F1', '#A9DFBF', '#F9E79F']
for box, color in zip(bp['boxes'], colors):
    box.set_facecolor(color)

# 叠加散点（jitter 抖动避免重叠）
for i, group in enumerate([group_a, group_b, group_c]):
    x = np.random.normal(i + 1, 0.04, size=len(group))  # 水平抖动
    plt.scatter(x, group, alpha=0.6, s=30,
                color='gray', edgecolors='black', linewidth=0.5)

plt.title("箱线图 + 数据点叠加", fontsize=14)
plt.grid(True, alpha=0.3)
plt.show()


# ============================================================
# 6. 水平箱线图
# ============================================================
# vert=False 让箱子横过来，适合标签长的场景

np.random.seed(42)
data = [np.random.normal(70, 10, 40) for _ in range(4)]
labels = ['TensorFlow', 'PyTorch', 'PaddlePaddle', 'MindSpore']

plt.figure(6, figsize=(8, 5))
plt.boxplot(data, tick_labels=labels, vert=False, patch_artist=True)
plt.title("各框架训练效果对比（横向箱线图）", fontsize=13)
plt.xlabel("准确率 (%)")
plt.grid(True, alpha=0.3)
plt.show()


# ============================================================
# 7. 综合练习：实验数据对比分析
# ============================================================
print("\n====== 综合练习：实验数据对比分析 ======")

np.random.seed(42)

# 模拟 A/B/C 三种算法的运行时间（毫秒）
algo_a = np.random.exponential(50, 30)   # 指数分布，偏态
algo_b = np.random.normal(40, 5, 30)     # 正态分布，稳定
algo_c = np.random.gamma(2, 30, 30)      # 伽马分布

# 加一些异常值模拟偶然卡顿
algo_a = np.append(algo_a, [200, 250])
algo_c = np.append(algo_c, [180, 220, 300])

plt.figure(7, figsize=(10, 6))

bp = plt.boxplot([algo_a, algo_b, algo_c],
                 tick_labels=['算法A', '算法B', '算法C'],
                 patch_artist=True, notch=True,
                 showmeans=True,
                 meanprops=dict(marker='D', markerfacecolor='red', markersize=7))

colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF']
for box, color in zip(bp['boxes'], colors):
    box.set_facecolor(color)

# 叠加散点
for i, group in enumerate([algo_a, algo_b, algo_c]):
    x = np.random.normal(i + 1, 0.05, size=len(group))
    plt.scatter(x, group, alpha=0.5, s=25, color='gray')

plt.title("算法运行时间对比（ms）", fontsize=14)
plt.ylabel("运行时间 (ms)")
plt.grid(True, alpha=0.3)

# 标注统计分析
medians = [np.median(g) for g in [algo_a, algo_b, algo_c]]
for i, med in enumerate(medians):
    plt.text(i + 1, med + 5, f'中位数\n{med:.0f}ms',
             ha='center', fontsize=9, color='darkred')

plt.tight_layout()
plt.savefig("algorithm_comparison.png", dpi=150)
plt.show()

print("运行时间统计:")
for name, g in zip(['算法A', '算法B', '算法C'], [algo_a, algo_b, algo_c]):
    print(f"  {name}: 中位数={np.median(g):.0f}ms, "
          f"均值={np.mean(g):.0f}ms, "
          f"IQR={np.percentile(g, 75)-np.percentile(g, 25):.0f}ms")
print("算法比较图已保存为 algorithm_comparison.png")


print("\n--- Day 10 箱线图补充完成！今天学了：")
print("  * plt.boxplot() — 基本箱线图")
print("  * 箱线图的5个统计量：Q1, Q2(中位数), Q3, 上下边缘, 异常值")
print("  * 多组对比 boxplot([g1, g2, g3])")
print("  * 美化：patch_artist, notch, showmeans, 颜色填充")
print("  * 箱线图 + 散点叠加")
print("  * vert=False 水平箱线图")

# ============================================================
# 额外：快速判断偏态
# ============================================================
# 中位数在箱子正中间 → 对称分布
# 中位数偏上（靠近Q3） → 左偏（负偏态）
# 中位数偏下（靠近Q1） → 右偏（正偏态）
# 异常值多在上方 → 右偏
# 异常值多在下方 → 左偏
