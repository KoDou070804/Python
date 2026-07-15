"""
Day 5: 面向对象
"""

# ── 1. 定义类 ──
print("─" * 40)
print("  定义类")
print("─" * 40)


class Student:
    school = "南邮"

    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def introduce(self):
        print(f"  我是{self.name}，{self.age}岁，来自{Student.school}")

    def is_pass(self):
        return self.score >= 60


s1 = Student("张三", 19, 85)
s2 = Student("李四", 20, 45)
s1.introduce()
print(f"  {s1.name} 及格: {s1.is_pass()}")
print(f"  {s2.name} 及格: {s2.is_pass()}")

# ── 2. 继承 ──
print("\n" + "─" * 40)
print("  继承")
print("─" * 40)


class GoodStudent(Student):
    def __init__(self, name, age, score, award):
        super().__init__(name, age, score)
        self.award = award

    def show_off(self):
        print(f"  我拿过{self.award}！")


g = GoodStudent("王五", 19, 95, "ACM校赛一等奖")
g.introduce()
g.show_off()
