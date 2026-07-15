"""
循环综合应用：发工资
规则：20名员工，每人绩效随机1-10
绩效 >= 6 发1000，< 6 不发，余额不足则停止
"""

import random

money = 10000
for i in range(1, 21):
    if money == 0:
        print("余额为0，发薪结束")
        break

    score = random.randint(1, 10)
    if score < 6:
        print(f"员工{i} 绩效{score}分，不发")
        continue

    if money >= 1000:
        money -= 1000
        print(f"员工{i} 发1000元 余额: {money}")
    else:
        print(f"余额不足({money}元)，停止发薪")
        break
