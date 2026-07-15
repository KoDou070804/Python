"""
Day 8: NumPy（一）— 创建数组、索引切片、基本运算
"""

import numpy as np

print("=" * 50)
print("1. 创建数组")
print("=" * 50)

# 从列表创建
arr1 = np.array([1, 2, 3, 4, 5])
print("np.array([1,2,3,4,5]):", arr1)

# 二维数组
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print("二维数组:\n", arr2)

# 全零数组
zeros = np.zeros((3, 4))  # 3行4列
print("np.zeros((3,4)):\n", zeros)

# 全1数组
ones = np.ones((2, 3))
print("np.ones((2,3)):\n", ones)

# 单位矩阵
eye = np.eye(3)
print("np.eye(3):\n", eye)

# 等差数列 — arange (类似range)
ar = np.arange(0, 10, 2)  # start, stop, step
print("np.arange(0,10,2):", ar)

# 等差数列 — linspace (指定个数)
ls = np.linspace(0, 1, 5)  # 从0到1，均匀取5个数
print("np.linspace(0,1,5):", ls)

# 随机数组
rand = np.random.randn(3, 3)  # 标准正态分布
print("np.random.randn(3,3):\n", rand)

print("\n" + "=" * 50)
print("2. 数组属性")
print("=" * 50)

a = np.array([[1, 2, 3], [4, 5, 6]])
print("数组:\n", a)
print("shape (形状):", a.shape)      # (2, 3)
print("dtype (数据类型):", a.dtype)   # int64
print("ndim (维度数):", a.ndim)       # 2
print("size (元素总数):", a.size)     # 6

# 指定数据类型
b = np.array([1, 2, 3], dtype=float)
print("\n指定 dtype=float:", b, "-> dtype:", b.dtype)

print("\n" + "=" * 50)
print("3. 索引与切片")
print("=" * 50)

arr = np.array([10, 20, 30, 40, 50])
print("一维数组:", arr)
print("arr[0]:", arr[0])       # 第一个元素
print("arr[-1]:", arr[-1])     # 最后一个
print("arr[1:4]:", arr[1:4])   # 切片 [20 30 40]
print("arr[:3]:", arr[:3])     # 前三个
print("arr[::2]:", arr[::2])   # 步长为2

# 二维索引
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\n二维数组:\n", arr2d)
print("arr2d[0,1]:", arr2d[0, 1])     # 第0行第1列 → 2
print("arr2d[1]:", arr2d[1])          # 第1行 → [4 5 6]
print("arr2d[:, 0]:", arr2d[:, 0])    # 所有行的第0列 → [1 4 7]
print("arr2d[0:2, 1:3]:\n", arr2d[0:2, 1:3])  # 前2行，第1-2列

# 花式索引 (fancy indexing)
print("\n花式索引:")
idx = np.array([0, 2, 4])
arr_f = np.array([10, 20, 30, 40, 50])
print("arr_f[[0,2,4]]:", arr_f[idx])  # 取出第0,2,4个

# 布尔索引
print("\n布尔索引:")
arr_b = np.array([1, 2, 3, 4, 5])
mask = arr_b > 3
print("arr_b > 3:", mask)
print("arr_b[arr_b > 3]:", arr_b[arr_b > 3])  # [4 5]
print("arr_b[(arr_b > 2) & (arr_b < 5)]:", arr_b[(arr_b > 2) & (arr_b < 5)])

print("\n" + "=" * 50)
print("4. 基本运算")
print("=" * 50)

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

print("x =", x)
print("y =", y)
print("x + y =", x + y)
print("x * y =", x * y)      # 逐元素乘法（不是矩阵乘法）
print("x ** 2 =", x ** 2)
print("np.sqrt(x) =", np.sqrt(x))
print("np.sum(x) =", np.sum(x))
print("np.mean(x) =", np.mean(x))
print("np.max(x) =", np.max(x))

# 广播 (broadcasting) — 不同形状也能算
print("\n广播:")
m = np.array([[1, 2, 3], [4, 5, 6]])
print("m =\n", m)
print("m + 10 =\n", m + 10)       # 标量广播
print("m + [10, 20, 30] =\n", m + np.array([10, 20, 30]))  # 行广播

print("\n" + "=" * 50)
print("5. 练习: 数组统计")
print("=" * 50)

# 生成 10 个学生的考试成绩 (0-100)
scores = np.random.randint(40, 100, size=10)
print("成绩:", scores)
print("最高分:", np.max(scores))
print("最低分:", np.min(scores))
print("平均分:", np.mean(scores))
print("标准差:", np.std(scores))
print("及格人数 (>60):", np.sum(scores > 60))
print("不及格成绩:", scores[scores < 60])
