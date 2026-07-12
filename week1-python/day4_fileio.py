# Day 4 速查卡 — 文件读写

## 1. 读取文件
# with 语句会自动关闭文件，推荐！
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()        # 读整个文件为字符串
    print(content)

with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()     # 读所有行到列表
    for line in lines:
        print(line.strip())   # strip() 去掉换行符


## 2. 写入文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# "w" 模式会覆盖，追加用 "a"
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("追加一行\n")


## 3. 练习模板：读取数字文件并统计
# 假设 numbers.txt 内容：
# 85
# 92
# 78
# 88
# 95

def analyze_scores(filename):
    """读文件中的分数，返回统计结果"""
    scores = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            scores.append(int(line.strip()))

    return {
        "总数": len(scores),
        "总分": sum(scores),
        "平均": sum(scores) / len(scores),
        "最高": max(scores),
        "最低": min(scores)
    }

# 测试
result = analyze_scores("numbers.txt")
for k, v in result.items():
    print(f"{k}: {v}")
