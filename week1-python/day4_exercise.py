def process_scores(filename='numbers.txt'):
    scores=[]
    with open(filename,'r',encoding='utf—8')as f:
        for line in f:
            line=line.strip()
            if line:
                scores.append(int(line))

    if not scores:
        print("文件中没有有效分数！")
        return
    #1.计算平均分
    avg=sum(scores)/len(scores)

    #2.统计及格人数（>=60）
    pass_count=sum(1 for s in scores if s>=60)

    #3.提取不及格分数（<=60）并写入fail.txt
    fails=[s for s in scores if s<60]
    with open('fail.txt','w',encoding='utf-8')as f:
        for score in fails:
            f.write(f"{score}\n")

    # 4. 提取优秀分数 (>=90) 并写入 excellent.txt
    excellents = [s for s in scores if s >= 90]
    with open('excellent.txt', 'w', encoding='utf-8') as f:
         for score in excellents:
            f.write(f"{score}\n")

    #输出到控制台
    print(f"平均分：{avg:.1f},及格人数：{pass_count}")
    print(f"不及格分数已写入fail.txt，共{len(fails)}人")
    print(f"优秀分数已写入excellent.txt,共{len(excellents)}人")

process_scores('numbers.txt')
