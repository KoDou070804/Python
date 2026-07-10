"""
BMI 计算器 - 交互式版本
"""

def calculate_bmi(weight, height):
    """计算 BMI"""
    if height <= 0 or weight <= 0:
        raise ValueError("身高和体重必须大于0")
    return weight / (height ** 2)


def main():
    try:
        # 交互式输入
        weight = float(input("请输入体重 (kg): "))
        height = float(input("请输入身高 (m): "))

        bmi = calculate_bmi(weight, height)
        print(f"\n体重: {weight}kg")
        print(f"身高: {height}m")
        print(f"BMI: {bmi:.1f}")

        if bmi < 18.5:
            print("分类: 偏瘦")
        elif bmi < 24:
            print("分类: 正常")
        elif bmi < 28:
            print("分类: 超重")
        else:
            print("分类: 肥胖")

    except ValueError as e:
        print(f"错误: {e}")
    except KeyboardInterrupt:
        print("\n程序已退出")


if __name__ == "__main__":
    main()