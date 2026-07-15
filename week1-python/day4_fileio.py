"""
Day 4: 文件读写
"""

# ── 1. 写入文件 ──
print("─" * 40)
print("  写入文件")
print("─" * 40)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

with open("output.txt", "a", encoding="utf-8") as f:
    f.write("追加一行\n")

print("  output.txt 已写入 3 行")

# ── 2. 读取文件 ──
print("\n" + "─" * 40)
print("  读取文件")
print("─" * 40)

with open("output.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(f"  → {line.strip()}")

# ── 3. 练习：分数统计 ──
print("\n" + "─" * 40)
print("  练习：分数统计")
print("─" * 40)

# 先生成一个数字文件
scores = [85, 92, 78, 88, 95]
with open("numbers.txt", "w", encoding="utf-8") as f:
    for s in scores:
        f.write(f"{s}\n")


def analyze_scores(filename):
    scores = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            scores.append(int(line.strip()))

    return {
        "总数": len(scores),
        "总分": sum(scores),
        "平均": sum(scores) / len(scores),
        "最高": max(scores),
        "最低": min(scores),
    }


result = analyze_scores("numbers.txt")
for k, v in result.items():
    print(f"  {k}: {v}")
