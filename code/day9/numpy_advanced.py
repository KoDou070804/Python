"""
Day 9: NumPy（二）— 矩阵运算 · 形状操作 · 高级技巧
"""

import numpy as np

print("=" * 60)
print("1. 矩阵运算进阶")
print("=" * 60)

# 点积 (dot product) — 真正的矩阵乘法
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print("A =\n", a)
print("B =\n", b)
print("A @ B (矩阵乘法):\n", a @ b)       # @ 是 Python 3.5+ 的矩阵乘法运算符
print("np.dot(A, B):\n", np.dot(a, b))   # 等价写法

# 转置
print("\nA 的转置:\n", a.T)
print("A.transpose():\n", a.transpose())

# 一维向量的点积
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print("\nx · y =", np.dot(x, y))         # 1*4 + 2*5 + 3*6 = 32

# 逆矩阵
c = np.array([[4, 7], [2, 6]])
c_inv = np.linalg.inv(c)
print("\nC =\n", c)
print("C^(-1) =\n", c_inv)
print("C @ C^(-1) (应为单位矩阵):\n", c @ c_inv)

# 解线性方程组: 3x + y = 9, x + 2y = 8
# 用矩阵表示: A @ [x, y]ᵀ = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
solution = np.linalg.solve(A, b)
print("\n解方程组 3x+y=9, x+2y=8:")
print(f"x = {solution[0]}, y = {solution[1]}")  # x=2, y=3
print("验证:", A @ solution)  # 应为 [9, 8]

# 行列式
print("\ndet(C) =", np.linalg.det(c))

# 特征值和特征向量
eigvals, eigvecs = np.linalg.eig(c)
print("特征值:", eigvals)
print("特征向量:\n", eigvecs)

print("\n" + "=" * 60)
print("2. 数组形状操作")
print("=" * 60)

arr = np.arange(12)
print("原始 (1D):", arr)

# reshape — 改变形状（返回新数组）
r = arr.reshape(3, 4)
print("\nreshape(3,4):\n", r)

# reshape(-1, n) — 自动推断维度
r2 = arr.reshape(-1, 3)  # 4行3列
print("reshape(-1,3):\n", r2)

# flatten — 展平为一维（返回副本）
flat = r.flatten()
print("\nflatten:", flat)

# ravel — 展平为一维（返回视图，修改影响原数组）
rav = r.ravel()
print("ravel:", rav)

# resize — 直接修改原数组形状（不返回新数组）
arr2 = np.arange(8).copy()
arr2.resize(2, 4)
print("\nresize(2,4):\n", arr2)

# newaxis — 增加维度
v = np.array([1, 2, 3])
print("\nnewaxis 增加维度:")
print("原始 shape:", v.shape)
print("v[:, np.newaxis] shape:", v[:, np.newaxis].shape)  # (3,1)
print("v[np.newaxis, :] shape:", v[np.newaxis, :].shape)  # (1,3)

print("\n" + "=" * 60)
print("3. 合并与拆分")
print("=" * 60)

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# 垂直堆叠
print("vstack:\n", np.vstack((a, b)))

# 水平堆叠
print("hstack:\n", np.hstack((a, b)))

# concatenate — 通用拼接
print("concatenate axis=0:\n", np.concatenate((a, b), axis=0))
print("concatenate axis=1:\n", np.concatenate((a, b), axis=1))

# stack — 沿新轴堆叠
c = np.stack((a, b))
print("stack (新轴):\n", c, "shape:", c.shape)

# split — 拆分
arr = np.arange(10)
splits = np.split(arr, [3, 7])  # 在索引 3 和 7 处切分
print("\nsplit [3,7]:", splits)

# vsplit / hsplit
arr2d = np.arange(16).reshape(4, 4)
print("\n原始 (4x4):\n", arr2d)
print("hsplit 切成4列:\n", np.hsplit(arr2d, 4))
print("vsplit 切成2块:\n", np.vsplit(arr2d, 2))

print("\n" + "=" * 60)
print("4. 高级索引与排序")
print("=" * 60)

arr = np.array([10, 30, 20, 50, 40])
print("原始:", arr)

# np.where — 条件索引（类似三元表达式）
print("np.where(arr > 25, 1, 0):", np.where(arr > 25, 1, 0))
print("np.where(arr > 25)[0]:", np.where(arr > 25))  # 返回索引元组

# argmax / argmin — 返回最大/最小值的索引
print("argmax (最大索引):", np.argmax(arr))  # 3 (50)
print("argmin (最小索引):", np.argmin(arr))  # 0 (10)

# argsort — 返回排序后的索引
print("argsort (排序索引):", np.argsort(arr))

# sort — 排序
print("sort 排序:", np.sort(arr))

# 二维排序
arr2d = np.array([[3, 1, 2], [6, 5, 4]])
print("\n二维:\n", arr2d)
print("sort axis=0:\n", np.sort(arr2d, axis=0))
print("sort axis=1:\n", np.sort(arr2d, axis=1))

# 沿轴取最大/最小
print("max axis=0:", arr2d.max(axis=0))  # 每列最大
print("max axis=1:", arr2d.max(axis=1))  # 每行最大

print("\n" + "=" * 60)
print("5. 随机数深入")
print("=" * 60)

# 设置种子 — 结果可复现
np.random.seed(42)
print("固定种子的随机 (42):", np.random.randn(3))

# 常用分布
print("\n均匀分布 [0,1):", np.random.rand(5))
print("N(0,1) 正态分布:", np.random.randn(5))
print("均匀整数 [1,100]:", np.random.randint(1, 100, 10))

# shuffle — 打乱（原地修改）
cards = np.arange(10)
np.random.shuffle(cards)
print("\nshuffle 打乱:", cards)

# choice — 随机选择
choices = np.random.choice(['正面', '反面'], size=10)
print("choice 随机选择:", choices)
# 带权重的选择
weighted = np.random.choice(['A', 'B', 'C'], size=10, p=[0.5, 0.3, 0.2])
print("带权重选择:", weighted)

# 随机抽样
data = np.arange(100)
sample = np.random.choice(data, size=5, replace=False)  # 不放回
print("不放回抽样:", sample)

print("\n" + "=" * 60)
print("6. 综合练习：学生成绩分析")
print("=" * 60)

np.random.seed(2026)
# 生成 5 个班，每班 30 人的成绩 (0-100)
scores = np.random.randint(30, 100, size=(5, 30))
print("成绩矩阵:", scores.shape)

# 各班平均分
class_means = scores.mean(axis=1)
print("各班平均分:", np.round(class_means, 1))

# 最高分、最低分
print("年级最高分:", scores.max())
print("年级最低分:", scores.min())

# 每个班的最高/最低
print("各班最高分:", scores.max(axis=1))
print("各班最低分:", scores.min(axis=1))

# 每个班的及格率
pass_counts = np.sum(scores >= 60, axis=1)
pass_rates = pass_counts / scores.shape[1] * 100
print("各班及格率:", np.round(pass_rates, 1))

# 优秀率 (>=90)
excellent = np.sum(scores >= 90, axis=1)
print("各班优秀人数:", excellent)

# 标准差 — 看出哪个班成绩分化最严重
stds = scores.std(axis=1)
print("各班标准差:", np.round(stds, 1))
print("成绩分化最大的班: 第", np.argmax(stds) + 1, "班")

# 年级排名前 10
all_scores = scores.flatten()
all_scores.sort()
print("年级前十名:", all_scores[-10:])
