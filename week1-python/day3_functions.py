# Day 3 速查卡 — 函数 & 作用域

## 1. 定义和调用函数
def greet(name):
    """给 name 打个招呼"""  # 文档字符串（可选）
    return f"你好, {name}!"

print(greet("小明"))       # 你好, 小明!
print(greet("小红"))       # 你好, 小红!


## 2. 参数类型
# 默认参数
def power(base, exp=2):
    return base ** exp

print(power(3))       # 9 (3²)
print(power(3, 3))    # 27 (3³)


# 多个返回值（实际是元组）
def stats(a, b, c):
    total = a + b + c
    avg = total / 3
    return total, avg   # 返回元组

s, a = stats(80, 90, 85)   # 解包接收
print(f"总分: {s}, 平均: {a}")


## 3. 变量作用域
x = 10  # 全局变量

def show():
    y = 5           # 局部变量，仅在函数内有效
    print(f"内部: x={x}, y={y}")  # 内部可以读全局的 x

show()
# print(y)  # 报错！y 在外部不存在


# 修改全局变量需要用 global
count = 0

def add_one():
    global count    # 声明要修改全局变量
    count += 1

add_one()
add_one()
print(count)  # 2
