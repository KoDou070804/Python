"""
Day 6-7: 学生成绩管理系统 — OOP + 文件 + lambda + 推导式综合应用
"""

import json
import os

# ═══════════════════════════════════
# 1. 学生类
# ═══════════════════════════════════


class Student:
    def __init__(self, name, sid, scores):
        self.name = name
        self.sid = sid
        self.scores = scores

    def total(self):
        return sum(self.scores.values())

    def average(self):
        return round(self.total() / len(self.scores), 1)

    def all_passed(self, line=60):
        return all(s >= line for s in self.scores.values())

    def to_dict(self):
        return {"name": self.name, "sid": self.sid, "scores": self.scores}

    @staticmethod
    def from_dict(data):
        return Student(data["name"], data["sid"], data["scores"])

    def __str__(self):
        return f"{self.sid} {self.name} | 总分: {self.total()} 平均: {self.average()}"


# ═══════════════════════════════════
# 2. 数据管理类
# ═══════════════════════════════════


class Manager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self._load()

    # ── 文件操作 ──
    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.students = [Student.from_dict(item) for item in json.load(f)]
            print(f"已读取 {len(self.students)} 条记录")
        else:
            print("未找到数据文件，初始化为空")

    def save(self):
        data = [s.to_dict() for s in self.students]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("数据已保存")

    # ── CRUD ──
    def add(self, name, sid, scores):
        if any(s.sid == sid for s in self.students):
            print(f"学号 {sid} 已存在")
            return
        stu = Student(name, sid, scores)
        self.students.append(stu)
        print(f"添加成功: {stu}")

    def delete(self, sid):
        before = len(self.students)
        self.students = [s for s in self.students if s.sid != sid]
        print(f"已删除学号 {sid}" if len(self.students) < before else f"未找到学号 {sid}")

    def find(self, sid):
        for s in self.students:
            if s.sid == sid:
                return s
        return None

    def update(self, sid, new_name=None, new_scores=None):
        s = self.find(sid)
        if not s:
            print("学号不存在")
            return
        if new_name:
            s.name = new_name
        if new_scores:
            s.scores.update(new_scores)
        print(f"修改成功: {s}")

    def list_all(self):
        if not self.students:
            print("暂无学生")
            return
        print("\n==== 全部学生 ====")
        for s in self.students:
            print(s)
        print("==================\n")

    # ── 排序与筛选 ──
    def sort_by_total(self, reverse=True):
        self.students.sort(key=lambda s: s.total(), reverse=reverse)
        print(f"已按总分{'降序' if reverse else '升序'}排列")
        self.list_all()

    def filter_by(self, condition):
        result = [s for s in self.students if condition(s)]
        print(f"\n==== 筛选结果 (共 {len(result)} 人) ====")
        for s in result:
            print(s)
        print("============================\n")
        return result

    # ── 统计 ──
    def statistics(self):
        if not self.students:
            print("无数据")
            return
        totals = [s.total() for s in self.students]
        all_scores = [v for s in self.students for v in s.scores.values()]
        pass_count = sum(1 for s in self.students if s.all_passed())

        print("\n====== 班级统计 ======")
        print(f"学生总数: {len(self.students)}")
        print(f"总分平均: {sum(totals) / len(totals):.1f}")
        print(f"全科及格: {pass_count}人 ({pass_count / len(self.students) * 100:.1f}%)")
        print(f"单科最高: {max(all_scores)}  最低: {min(all_scores)}")
        print("======================\n")


# ═══════════════════════════════════
# 3. 交互菜单
# ═══════════════════════════════════


def main():
    mgr = Manager()

    menu = """
请选择操作:
1. 添加学生    2. 删除学生    3. 修改学生
4. 查找学生    5. 列出全部    6. 总分排序
7. 筛选(总分>=)  8. 班级统计  9. 退出
请输入数字: """

    while True:
        choice = input(menu).strip()

        if choice == "1":
            name = input("姓名: ")
            sid = input("学号: ")
            try:
                scores = {
                    "语文": float(input("语文成绩: ")),
                    "数学": float(input("数学成绩: ")),
                    "英语": float(input("英语成绩: ")),
                }
            except ValueError:
                print("成绩必须为数字")
                continue
            mgr.add(name, sid, scores)

        elif choice == "2":
            mgr.delete(input("要删除的学号: "))

        elif choice == "3":
            sid = input("要修改的学号: ")
            new_name = input("新姓名(不修直接回车): ") or None
            new_scores = {}
            for sub in ["语文", "数学", "英语"]:
                val = input(f"新{sub}成绩(不修直接回车): ")
                if val:
                    new_scores[sub] = float(val)
            mgr.update(sid, new_name, new_scores if new_scores else None)

        elif choice == "4":
            s = mgr.find(input("要查找的学号: "))
            print(s if s else "未找到")

        elif choice == "5":
            mgr.list_all()

        elif choice == "6":
            mgr.sort_by_total()

        elif choice == "7":
            try:
                mgr.filter_by(lambda s: s.total() >= float(input("显示总分 >= ")))
            except ValueError:
                print("请输入数字")

        elif choice == "8":
            mgr.statistics()

        elif choice == "9":
            mgr.save()
            print("再见!")
            break
        else:
            print("无效输入")


if __name__ == "__main__":
    main()
