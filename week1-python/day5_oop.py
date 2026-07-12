# Day 5 速查卡 — 面向对象

## 1. 定义类
class Student:
    """学生类"""
    school = "南邮"  # 类属性（所有实例共享）

    def __init__(self, name, age, score):
        self.name = name   # 实例属性
        self.age = age
        self.score = score

    def introduce(self):
        """实例方法 — 第一个参数永远是 self"""
        print(f"我是{self.name}，{self.age}岁，来自{Student.school}")

    def is_pass(self):
        return self.score >= 60


# 创建对象
s1 = Student("张三", 19, 85)
s2 = Student("李四", 20, 45)

s1.introduce()                    # 我是张三，19岁，来自南邮
print(s1.is_pass())               # True
print(s2.is_pass())               # False


## 2. 继承
class GoodStudent(Student):
    """好学生=学生+额外能力"""

    def __init__(self, name, age, score, award):
        super().__init__(name, age, score)  # 调用父类构造函数
        self.award = award

    def show_off(self):
        print(f"我拿过{self.award}！")


g = GoodStudent("王五", 19, 95, "ACM校赛一等奖")
g.introduce()      # 继承来的方法
g.show_off()       # 自己的方法
