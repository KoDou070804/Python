# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

print("="*50)
print("1. 创建 DataFrame（从字典）")
print("="*50)
data = {
    '姓名': ['张三', '李四', '王五', '赵六', '陈七'],
    '数学': [88, 92, 75, 95, 80],
    '英语': [76, 88, 90, 82, 85],
    '物理': [91, 79, 84, 93, 78]
}
df = pd.DataFrame(data)
print(df)
print(f"\n形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"行索引: {list(df.index)}")

print("\n" + "="*50)
print("2. Series — 一维数据")
print("="*50)
scores = pd.Series([88, 92, 75, 95, 80], index=['张三', '李四', '王五', '赵六', '陈七'], name='数学成绩')
print(scores)
print(f"\n最大值: {scores.max()}")
print(f"最小值: {scores.min()}")
print(f"平均值: {scores.mean():.1f}")
print(f"标准差: {scores.std():.1f}")

print("\n" + "="*50)
print("3. 从文件创建（这里用 CSV 字符串模拟）")
print("="*50)
from io import StringIO
csv_data = """姓名,数学,英语,物理
张三,88,76,91
李四,92,88,79
王五,75,90,84
赵六,95,82,93
陈七,80,85,78"""
df_csv = pd.read_csv(StringIO(csv_data))
print(df_csv)

print("\n" + "="*50)
print("4. 数据预览")
print("="*50)
print("head():")
print(df.head(3))
print("\ninfo():")
print(df.info())
print("\ndescribe():")
print(df.describe().round(1))

print("\n" + "="*50)
print("5. 数据选择 -- 列选择")
print("="*50)
print("单列 (df['数学']):")
print(df['数学'])
print("\n多列 (df[['姓名', '数学']]):")
print(df[['姓名', '数学']])
print("\n属性语法 (df.数学):")
print(df.数学)

print("\n" + "="*50)
print("6. 数据选择 -- 行选择 (iloc / loc)")
print("="*50)
print("iloc[0] 第一行:")
print(df.iloc[0])
print("\niloc[1:3] 第2-3行:")
print(df.iloc[1:3])
print("\nloc[1:3] 按标签（含末尾）:")
print(df.loc[1:3])
print("\nloc[0, ['姓名', '数学']] 指定行列:")
print(df.loc[0, ['姓名', '数学']])

print("\n" + "="*50)
print("7. 布尔索引 -- 条件筛选")
print("="*50)
print("数学 > 85 的同学:")
print(df[df['数学'] > 85])
print("\n数学 > 85 且英语 > 80:")
print(df[(df['数学'] > 85) & (df['英语'] > 80)])
print("\n数学 > 90 或物理 > 90:")
print(df[(df['数学'] > 90) | (df['物理'] > 90)])

print("\n" + "="*50)
print("8. 基本统计操作")
print("="*50)
# 新增一列: 平均分
df['平均分'] = df[['数学', '英语', '物理']].mean(axis=1).round(1)
print("添加'平均分'列后:")
print(df)
print(f"\n各科平均分:\n{df[['数学', '英语', '物理']].mean()}")
print(f"\n各科最高分:\n{df[['数学', '英语', '物理']].max()}")
print(f"\n按数学排序 (降序):")
print(df.sort_values('数学', ascending=False)[['姓名', '数学', '平均分']])
