"""
Day 3: 函数 · 作用域
"""

# ── 1. 定义和调用 ──
print("─" * 40)
print("  定义和调用")
print("─" * 40)


def greet(name):
    return f"你好, {name}!"


print(f"  greet('小明'): {greet('小明')}")
print(f"  greet('小红'): {greet('小红')}")

# ── 2. 默认参数 ──
print("\n" + "─" * 40)
print("  默认参数")
print("─" * 40)


def power(base, exp=2):
    return base ** exp


print(f"  power(3) = {power(3)}      # 3 的 2 次方")
print(f"  power(3,3) = {power(3, 3)}   # 3 的 3 次方")

# ── 3. 多个返回值 ──
print("\n" + "─" * 40)
print("  多个返回值")
print("─" * 40)


def stats(a, b, c):
    total = a + b + c
    avg = total / 3
    return total, avg


s, a = stats(80, 90, 85)
print(f"  总分: {s}, 平均: {a}")

# ── 4. 作用域 ──
print("\n" + "─" * 40)
print("  变量作用域")
print("─" * 40)

x = 10  # 全局变量


def show():
    y = 5
    print(f"  函数内部: x={x}, y={y}")  # 内部可读全局


show()

count = 0


def add_one():
    global count
    count += 1


add_one()
add_one()
print(f"  global count 两次自增后: {count}")
