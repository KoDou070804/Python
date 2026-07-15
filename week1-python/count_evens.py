"""
统计 1-100 中有几个偶数
"""

count = sum(1 for i in range(1, 100) if i % 2 == 0)
print(f"1-100 中有 {count} 个偶数")
