"""
Day 4 练习：分数读取 + 统计 + 筛选写入
"""

import os

# 先生成测试数据
scores_data = [85, 92, 78, 45, 88, 95, 34, 67, 91, 52]
with open("numbers.txt", "w", encoding="utf-8") as f:
    for s in scores_data:
        f.write(f"{s}\n")


def process_scores(filename="numbers.txt"):
    scores = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                scores.append(int(line))

    if not scores:
        print("文件中没有有效分数！")
        return

    avg = sum(scores) / len(scores)
    pass_count = sum(1 for s in scores if s >= 60)
    fails = [s for s in scores if s < 60]
    excellents = [s for s in scores if s >= 90]

    with open("fail.txt", "w", encoding="utf-8") as f:
        for score in fails:
            f.write(f"{score}\n")

    with open("excellent.txt", "w", encoding="utf-8") as f:
        for score in excellents:
            f.write(f"{score}\n")

    print(f"  平均分: {avg:.1f}")
    print(f"  及格人数: {pass_count}/{len(scores)}")
    print(f"  不及格: {len(fails)}人 → fail.txt")
    print(f"  优秀:   {len(excellents)}人 → excellent.txt")


process_scores()
