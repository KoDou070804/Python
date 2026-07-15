"""
Day 9: NumPy（二）— 矩阵运算 · 形状操作 · 高级技巧
"""

import numpy as np
np.set_printoptions(precision=2, suppress=True)

# ─────────────────────────────────────────────
# 1. 矩阵运算进阶
# ─────────────────────────────────────────────
print("─" * 48)
print("  1. 矩阵运算进阶")
print("─" * 48)

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(f"  A =\n{A}\n  B =\n{B}")
print(f"  A @ B:\n{A @ B}")

print(f"\n  转置 A.T:\n{A.T}")

x, y = np.array([1, 2, 3]), np.array([4, 5, 6])
print(f"\n  向量点积 x·y = {np.dot(x, y)}")

C = np.array([[4, 7], [2, 6]])
C_inv = np.linalg.inv(C)
print(f"\n  C^(-1):\n{C_inv}")
print(f"  C @ C^(-1):\n{C @ C_inv}")

A, b = np.array([[3, 1], [1, 2]]), np.array([9, 8])
sol = np.linalg.solve(A, b)
print(f"\n  解 3x+y=9, x+2y=8  →  x={sol[0]}, y={sol[1]}  验证: {A @ sol}")

print(f"\n  det(C) = {np.linalg.det(C)}")
eigvals, eigvecs = np.linalg.eig(C)
print(f"  特征值: {eigvals}")
print(f"  特征向量:\n{eigvecs}")

# ─────────────────────────────────────────────
# 2. 数组形状操作
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  2. 数组形状操作")
print("─" * 48)

arr = np.arange(12)
print(f"  原始: {arr}")
print(f"  reshape(3,4):\n{arr.reshape(3, 4)}")
print(f"  reshape(-1,3):\n{arr.reshape(-1, 3)}")

r = np.array([[1, 2, 3], [4, 5, 6]])
print(f"  flatten: {r.flatten()}")

v = np.array([1, 2, 3])
print(f"\n  newaxis:  {v.shape} → 列 {v[:, np.newaxis].shape}  行 {v[np.newaxis, :].shape}")

# ─────────────────────────────────────────────
# 3. 合并与拆分
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  3. 合并与拆分")
print("─" * 48)

a, b = np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])
print(f"  vstack:\n{np.vstack((a, b))}")
print(f"  hstack:\n{np.hstack((a, b))}")

arr2d = np.arange(16).reshape(4, 4)
print(f"\n  原始:\n{arr2d}")
print(f"  hsplit 切4列: {[x.shape for x in np.hsplit(arr2d, 4)]}")
print(f"  vsplit 切2块: {[x.shape for x in np.vsplit(arr2d, 2)]}")

# ─────────────────────────────────────────────
# 4. 高级索引与排序
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  4. 高级索引与排序")
print("─" * 48)

arr = np.array([10, 30, 20, 50, 40])
print(f"  原始: {arr}")
print(f"  argmax={np.argmax(arr)}  argmin={np.argmin(arr)}")
print(f"  argsort={np.argsort(arr)}  sort={np.sort(arr)}")
print(f"  where >25: {np.where(arr > 25)[0]}")

arr2d = np.array([[3, 1, 2], [6, 5, 4]])
print(f"\n  二维 axis:\n{arr2d}")
print(f"  sort axis=0:\n{np.sort(arr2d, axis=0)}")
print(f"  sort axis=1:\n{np.sort(arr2d, axis=1)}")

# ─────────────────────────────────────────────
# 5. 随机数深入
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  5. 随机数深入")
print("─" * 48)

np.random.seed(42)
print(f"  seed(42) randn(3): {np.random.randn(3)}")

print(f"  rand(5):    {np.random.rand(5)}")
print(f"  randn(5):   {np.random.randn(5)}")
print(f"  randint:    {np.random.randint(1, 100, 10)}")

cards = np.arange(10)
np.random.shuffle(cards)
print(f"  shuffle:    {cards}")

print(f"  choice:     {np.random.choice(['正面','反面'], size=10)}")
print(f"  不放回抽样: {np.random.choice(100, size=5, replace=False)}")

# ─────────────────────────────────────────────
# 6. 综合练习：成绩分析
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  6. 综合练习：学生成绩分析")
print("─" * 48)

np.random.seed(2026)
scores = np.random.randint(30, 100, size=(5, 30))
print(f"  成绩矩阵: {scores.shape}")

means = scores.mean(axis=1)
stds = scores.std(axis=1)
print(f"  各班均分: {np.round(means, 1)}")
print(f"  各班标准差: {np.round(stds, 1)}")
print(f"  分化最严重: 第{np.argmax(stds) + 1}班")

rank = np.sort(scores.flatten())
print(f"  年级前10: {rank[-10:]}")
print(f"  年级均分: {scores.mean():.1f}  最高: {scores.max()}  最低: {scores.min()}")
