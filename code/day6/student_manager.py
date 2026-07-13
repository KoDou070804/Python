import json
import os

# ==================== 1. 学生类 ====================
class Student:
    """学生类：存储一个学生的基本信息与成绩"""

    def __init__(self, name, sid, scores):
        self.name = name
        self.sid = sid
        self.scores = scores

    def total(self):
        return sum(self.scores.values())

    def average(self):
        return round(self.total() / len(self.scores), 1)

    def all_passed(self, line=60):
        return all(score >= line for score in self.scores.values())

    def to_dict(self):
        return {
            'name': self.name,
            'sid': self.sid,
            'scores': self.scores
        }

    @staticmethod
    def from_dict(data):
        return Student(data['name'], data['sid'], data['scores'])

    def __str__(self):
        return f"{self.sid} {self.name} | 总分：{self.total()} 平均：{self.average()}"


# ==================== 2. 数据管理类 ====================
class Manager:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = []
        self.load()

    # ---------- 文件操作 ----------
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self.students = [Student.from_dict(item) for item in raw_data]
            print(f"已读取 {len(self.students)} 条记录")
        else:
            print("未找到数据文件，初始化为空")

    def save(self):
        data = [stu.to_dict() for stu in self.students]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("数据已保存")

    # ---------- 增删改查 ----------
    def add(self, name, sid, scores):
        if any(s.sid == sid for s in self.students):
            print(f"学号 {sid} 已存在，无法添加")
            return
        stu = Student(name, sid, scores)
        self.students.append(stu)
        print(f"添加成功：{stu}")

    def delete(self, sid):
        before = len(self.students)
        self.students = [s for s in self.students if s.sid != sid]
        if len(self.students) < before:
            print(f"已删除学号 {sid} 的学生")
        else:
            print(f"未找到学号 {sid}")

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
        print(f"修改成功：{s}")

    def list_all(self):
        if not self.students:
            print("暂无学生")
            return
        print("\n==== 全部学生 ====")
        for s in self.students:
            print(s)
        print("==================\n")

    # ---------- 排序与筛选 ----------
    def sort_by_total(self, reverse=True):
        self.students.sort(key=lambda s: s.total(), reverse=reverse)
        print(f"已按总分{'降序' if reverse else '升序'}排列")
        self.list_all()

    def filter_by(self, condition_func):
        result = [s for s in self.students if condition_func(s)]
        print(f"\n==== 筛选结果（共 {len(result)} 人）====")
        for s in result:
            print(s)
        print("============================\n")
        return result

    # ---------- 统计 ----------
    def statistics(self):
        if not self.students:
            print("无数据，无法统计")
            return

        totals = [s.total() for s in self.students]
        avg_total = sum(totals) / len(totals)

        pass_count = sum(1 for s in self.students if s.all_passed())

        all_scores = [score for s in self.students for score in s.scores.values()]
        max_single = max(all_scores)
        min_single = min(all_scores)

        print("\n====== 班级统计 ======")
        print(f"学生总数：{len(self.students)}")
        print(f"总分平均分：{avg_total:.1f}")
        print(f"全科及格人数：{pass_count}")
        print(f"全科及格率：{pass_count / len(self.students) * 100:.1f}%")
        print(f"单科最高分：{max_single}")
        print(f"单科最低分：{min_single}")
        print("======================\n")


# ==================== 3. 主程序菜单 ====================
def main():
    mgr = Manager()

    menu = """
请选择操作：
1. 添加学生    2. 删除学生    3. 修改学生
4. 查找学生    5. 列出全部    6. 总分排序
7. 筛选(总分>=)  8. 班级统计  9. 退出
请输入数字："""

    while True:
        choice = input(menu).strip()

        if choice == '1':
            name = input("姓名：")
            sid = input("学号：")
            try:
                scores = {
                    '语文': float(input("语文成绩：")),
                    '数学': float(input("数学成绩：")),
                    '英语': float(input("英语成绩："))
                }
            except ValueError:
                print("成绩必须为数字，添加失败")
                continue
            mgr.add(name, sid, scores)

        elif choice == '2':
            sid = input("要删除的学号：")
            mgr.delete(sid)

        elif choice == '3':
            sid = input("要修改的学号：")
            print("不修改的项直接回车跳过")
            new_name = input("新姓名：")
            new_ch = input("新语文成绩：")
            new_ma = input("新数学成绩：")
            new_en = input("新英语成绩：")
            new_scores = {}
            if new_ch: new_scores['语文'] = float(new_ch)
            if new_ma: new_scores['数学'] = float(new_ma)
            if new_en: new_scores['英语'] = float(new_en)
            mgr.update(sid,
                       new_name if new_name else None,
                       new_scores if new_scores else None)

        elif choice == '4':
            sid = input("要查找的学号：")
            s = mgr.find(sid)
            print(s if s else "未找到该学生")

        elif choice == '5':
            mgr.list_all()

        elif choice == '6':
            mgr.sort_by_total()

        elif choice == '7':
            try:
                threshold = float(input("显示总分 >= "))
            except ValueError:
                print("请输入数字")
                continue
            mgr.filter_by(lambda s: s.total() >= threshold)

        elif choice == '8':
            mgr.statistics()

        elif choice == '9':
            mgr.save()
            print("再见！")
            break

        else:
            print("无效输入，请重新选择")


if __name__ == "__main__":
    main()
