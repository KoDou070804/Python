"""
Day 2: 列表 · 字典 · 元组 · 集合
"""

# ── 1. 列表 list ──
print("─" * 40)
print("  列表 list")
print("─" * 40)

nums = [1, 2, 3, 4, 5]
nums.append(6)            # 末尾追加
nums.insert(0, 0)         # 指定位置插入
nums.pop()                # 删除最后一个
nums.remove(3)            # 删除第一个匹配项
nums[0] = 99              # 修改

print(f"  最终列表: {nums}")
print(f"  nums[0]={nums[0]}  nums[-1]={nums[-1]}  nums[1:3]={nums[1:3]}")

# ── 2. 字典 dict ──
print("\n" + "─" * 40)
print("  字典 dict")
print("─" * 40)

stu = {"name": "张三", "age": 19, "score": 90}
stu["city"] = "南京"     # 新增
stu["age"] = 20           # 修改

print(f"  name={stu['name']}  age={stu['age']}  city={stu.get('city')}")

# ── 3. 元组 tuple ──
point = (10, 20)
x, y = point
print(f"\n  tuple 解包: point={point} → x={x}, y={y}")

# ── 4. 集合 set ──
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)
print(f"  set 去重: {nums} → {unique}")

# ── 练习：学生成绩管理 ──
print("\n" + "─" * 40)
print("  练习：学生成绩管理")
print("─" * 40)

students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]

total = sum(s["score"] for s in students)
for s in students:
    print(f"  {s['name']}: {s['score']}")
print(f"  平均分: {total / len(students):.1f}")
