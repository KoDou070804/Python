
"""
Day 10 — Matplotlib（一）
=========================
内容：折线图 · 散点图 · 图表基本设置
"""

import matplotlib.pyplot as plt
import numpy as np

# Windows 中文显示设置
plt.rcParams['font.family'] = 'Microsoft YaHei'   # 或者 'SimHei'
plt.rcParams['axes.unicode_minus'] = False         # 解决负号显示为方块

# ============================================================
# 1. 折线图 — plt.plot()
# ============================================================
# 折线图是最基本的图表类型，用来展示数据的变化趋势

# 1.1 最简单的折线图
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.figure(1)          # 创建一个新图表（编号1）
plt.plot(x, y)         # 绘制折线图
plt.title("基本折线图")
plt.show()             # 显示图表

# 1.2 带样式的折线图
# plot() 的第三个参数是格式字符串: '[颜色][标记][线型]'
# 颜色: r=红, g=绿, b=蓝, c=青, m=品红, y=黄, k=黑
# 标记: o=圆点, s=方块, ^=三角, x=叉, *=星号
# 线型: -=实线, --=虚线, :=点线, -.=点划线

x = np.linspace(0, 10, 20)       # 0到10均匀取20个点
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(2)
plt.plot(x, y1, 'ro--')          # 红色圆点+虚线
plt.plot(x, y2, 'bs-')           # 蓝色方块+实线
plt.title("带样式的折线图")
plt.legend(["sin(x)", "cos(x)"])  # 图例
plt.show()

# 1.3 用参数控制样式（更灵活）
plt.figure(3)
plt.plot(x, y1, color='red', linestyle='--', linewidth=2,
         marker='o', markersize=6, label='sin(x)')
plt.plot(x, y2, color='blue', linestyle='-', linewidth=1.5,
         marker='s', markersize=6, label='cos(x)')
plt.title("参数控制样式")
plt.legend()
plt.grid(True)                   # 显示网格
plt.show()

# ============================================================
# 2. 散点图 — plt.scatter()
# ============================================================
# 散点图显示两个变量之间的关系

# 2.1 基本散点图
n = 50
x = np.random.rand(n) * 10
y = np.random.rand(n) * 10

plt.figure(4)
plt.scatter(x, y)
plt.title("基本散点图")
plt.show()

# 2.2 带颜色和大小映射的散点图
n = 100
x = np.random.randn(n) * 5
y = np.random.randn(n) * 5
colors = np.random.rand(n)        # 颜色值
sizes = np.random.rand(n) * 500   # 点的大小

plt.figure(5)
scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6,
                      cmap='viridis')  # alpha=透明度, cmap=颜色映射
plt.colorbar(scatter)             # 显示颜色条
plt.title("散点图：颜色和大小映射")
plt.show()

# 2.3 用散点图看相关性
plt.figure(6)
# 正相关数据
x = np.random.randn(100)
y = x * 2 + np.random.randn(100) * 0.5

plt.scatter(x, y, alpha=0.6)
plt.title("正相关关系")
plt.xlabel("X 值")
plt.ylabel("Y 值")
plt.grid(True, alpha=0.3)
plt.show()

# ============================================================
# 3. 一张图上画多种图
# ============================================================
x = np.linspace(0, 10, 30)
y = 2 * x + 1 + np.random.randn(30) * 1.5   # 带噪声的线性数据
y_fit = 2 * x + 1                            # 拟合直线

plt.figure(7)
plt.scatter(x, y, color='blue', label='数据点', alpha=0.7)
plt.plot(x, y_fit, color='red', linestyle='--', linewidth=2,
         label='拟合线')
plt.title("数据点 + 拟合线")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# ============================================================
# 4. 图表基本设置总结
# ============================================================
# plt.title("文本")      — 标题
# plt.xlabel("文本")     — X轴标签
# plt.ylabel("文本")     — Y轴标签
# plt.legend()           — 图例（需要有 label 参数）
# plt.grid(True)         — 网格
# plt.xlim(最小值, 最大值) — X轴范围
# plt.ylim(最小值, 最大值) — Y轴范围
# plt.savefig("文件名")   — 保存图片
# plt.show()             — 显示图片
# plt.figure(编号)       — 新建/切换到指定图表
# plt.close()            — 关闭当前图表

# 一个完整的例子
x = np.linspace(0, 4*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

plt.figure(8, figsize=(8, 5))    # 设置图表大小（宽8英寸，高5英寸）
plt.plot(x, y_sin, 'b-', linewidth=2, label='sin(x)')
plt.plot(x, y_cos, 'r--', linewidth=2, label='cos(x)')
plt.title("正弦和余弦曲线", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("y", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.xlim(0, 4*np.pi)
plt.ylim(-1.5, 1.5)

# 添加注释
plt.axhline(y=0, color='black', linewidth=0.5)   # 水平参考线 y=0
plt.axvline(x=np.pi, color='gray', linestyle=':', alpha=0.7)  # 垂直参考线 x=π

plt.tight_layout()               # 自动调整布局
plt.savefig("sin_cos.png", dpi=150)  # 保存为图片
plt.show()

print("图表已保存为 sin_cos.png")

# ============================================================
# 5. 综合练习
# ============================================================
# 任务：模拟一个班级40人的两次考试成绩，
#       用散点图展示两次成绩的关系，画出平均线

print("\n====== 综合练习：成绩分析 ======")

np.random.seed(42)
# 期中成绩（0-100）
midterm = np.random.randint(40, 100, 40)
# 期末成绩 = 期中*0.6 + 努力程度 + 随机波动
effort = np.random.randn(40) * 5
final = midterm * 0.6 + 30 + effort
final = np.clip(final, 0, 100)   # 限制在0-100范围

plt.figure(9, figsize=(8, 6))
plt.scatter(midterm, final, alpha=0.7, c=midterm, cmap='coolwarm',
            s=80, label='学生')

# 画一条 y=x 的参考线（如果两次成绩一样）
plt.plot([0, 100], [0, 100], 'k--', alpha=0.3, label='y=x (持平线)')

# 标出平均分
mid_mean = np.mean(midterm)
final_mean = np.mean(final)
plt.axhline(final_mean, color='green', linestyle=':', alpha=0.6,
            label=f'期末平均分={final_mean:.1f}')
plt.axvline(mid_mean, color='orange', linestyle=':', alpha=0.6,
            label=f'期中平均分={mid_mean:.1f}')

plt.title("期中 vs 期末成绩分布", fontsize=14)
plt.xlabel("期中成绩", fontsize=12)
plt.ylabel("期末成绩", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# 在图上标注进步最大的学生
improvement = final - midterm
top_improver = np.argmax(improvement)
plt.annotate(f'进步最大\n{improvement[top_improver]:+.0f}分',
             xy=(midterm[top_improver], final[top_improver]),
             xytext=(midterm[top_improver]-15, final[top_improver]+10),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10)

plt.tight_layout()
plt.savefig("score_analysis.png", dpi=150)
plt.show()
print("成绩分析图已保存为 score_analysis.png")

print("\n--- Day 10 完成！今天学了：")
print("  * plt.plot() -- 折线图")
print("  * plt.scatter() -- 散点图")
print("  * 图表装饰：标题、标签、图例、网格、范围、保存")
print("  * 一张图上混合多种图")
