"""
Day 8: NumPy（一）— 创建数组 · 索引切片 · 基本运算
"""

import numpy as np
np.set_printoptions(precision=2, suppress=True)

# ─────────────────────────────────────────────
# 1. 创建数组
# ─────────────────────────────────────────────
print("─" * 48)
print("  1. 创建数组")
print("─" * 48)

arr1 = np.array([1, 2, 3, 4, 5])
print(f"  np.array([1,2,3,4,5]) → {arr1}")

arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print(f"  二维数组:\n{arr2}")

zeros = np.zeros((3, 4))
print(f"\n  zeros((3,4)):\n{zeros}")

ones = np.ones((2, 3))
print(f"\n  ones((2,3)):\n{ones}")

eye = np.eye(3)
print(f"\n  eye(3):\n{eye}")

ar = np.arange(0, 10, 2)
print(f"\n  arange(0,10,2) → {ar}")

ls = np.linspace(0, 1, 5)
print(f"  linspace(0,1,5) → {ls}")

rand = np.random.randn(3, 3)
print(f"\n  randn(3,3):\n{rand}")

# ─────────────────────────────────────────────
# 2. 数组属性
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  2. 数组属性")
print("─" * 48)

a = np.array([[1, 2, 3], [4, 5, 6]])
print(f"  shape: {a.shape}    dtype: {a.dtype}    ndim: {a.ndim}    size: {a.size}")

b = np.array([1, 2, 3], dtype=float)
print(f"  指定 float: {b}  →  dtype: {b.dtype}")

# ─────────────────────────────────────────────
# 3. 索引与切片
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  3. 索引与切片")
print("─" * 48)

arr = np.array([10, 20, 30, 40, 50])
print(f"  一维: {arr}")
print(f"  arr[0]={arr[0]}  arr[-1]={arr[-1]}  arr[1:4]={arr[1:4]}  arr[::2]={arr[::2]}")

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"\n  二维:\n{arr2d}")
print(f"  arr2d[0,1] = {arr2d[0, 1]}")
print(f"  arr2d[:, 0] = {arr2d[:, 0]}")
print(f"  arr2d[0:2, 1:3]:\n{arr2d[0:2, 1:3]}")

arr_f = np.array([10, 20, 30, 40, 50])
print(f"\n  花式索引 [0,2,4]: {arr_f[[0, 2, 4]]}")

arr_b = np.array([1, 2, 3, 4, 5])
print(f"  布尔索引 arr>3: {arr_b[arr_b > 3]}")

# ─────────────────────────────────────────────
# 4. 基本运算
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  4. 基本运算与广播")
print("─" * 48)

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print(f"  x={x}  y={y}")
print(f"  x+y={x+y}  x*y={x*y}  x**2={x**2}")
print(f"  sum={np.sum(x)}  mean={np.mean(x)}  max={np.max(x)}")

m = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n  广播:\n  m+10:\n{m + 10}")
print(f"  m+[10,20,30]:\n{m + np.array([10, 20, 30])}")

# ─────────────────────────────────────────────
# 5. 练习：成绩统计
# ─────────────────────────────────────────────
print("\n" + "─" * 48)
print("  5. 练习：成绩统计")
print("─" * 48)

np.random.seed(42)
scores = np.random.randint(40, 100, size=10)
print(f"  成绩: {scores}")
print(f"  平均: {scores.mean():.1f}  最高: {scores.max()}  最低: {scores.min()}")
print(f"  及格人数: {np.sum(scores > 60)}  不及格: {scores[scores < 60]}")
