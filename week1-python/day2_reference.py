# Day 2 速查卡 — 列表 & 字典

## 1. 列表 list
```python
# 创建
nums = [1, 2, 3, 4, 5]

# 增
nums.append(6)        # 末尾追加 → [1,2,3,4,5,6]
nums.insert(0, 0)     # 指定位置插入 → [0,1,2,3,4,5,6]

# 删
nums.pop()            # 删除最后一个
nums.remove(3)        # 删除第一个匹配的 3

# 改
nums[0] = 99

# 查
print(nums[0])        # 第一个
print(nums[-1])       # 最后一个
print(nums[1:3])      # 切片 [1:3] → 第2到第4个（不含3）

# 遍历
for n in nums:
    print(n)
```

## 2. 字典 dict
```python
# 创建
stu = {"name": "张三", "age": 19, "score": 90}

# 增/改
stu["city"] = "南京"   # 新增键
stu["age"] = 20        # 修改值

# 查
print(stu["name"])     # 取 value（key 不存在会报错）
print(stu.get("name")) # get 更安全，不存在返回 None

# 删
del stu["city"]

# 遍历
for key, value in stu.items():
    print(f"{key}: {value}")
```

## 3. 元组 tuple（不可变）
```python
point = (10, 20)
x, y = point          # 解包
```

## 4. 集合 set（去重）
```python
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)    # {1, 2, 3}
```

## 练习：学生成绩管理
```python
# 用 dict + list 存 3 个学生的信息，遍历打印
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78}
]
# 自己写遍历 + 算平均分
```
