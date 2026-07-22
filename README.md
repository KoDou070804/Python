# AI Learning Journey - Summer 2026

**目标**：进入南京邮电大学吴飞老师课题组，方向为多模态学习

---

## 学习日志

| Day | 日期 | 内容 | 完成情况 |
|-----|------|------|---------|
| 1 | 7.7 | 环境配置 + Python 基础：变量、条件、循环 | ✅ |
| 2 | 7.10 | 列表、字典、元组、集合 | ✅ |
| 3 | 7.12 | 函数、文件读写、面向对象 | ✅ |
| 4 | 7.13 | 进阶技巧：推导式、lambda、map/filter、装饰器 | ✅ |
| 5 | 7.14 | 综合练习：学生成绩管理系统（OOP版） | ✅ |
| 6 | 7.15 | NumPy：矩阵运算、形状操作、随机数 | ✅ |
| 7 | 7.17 | Matplotlib：箱线图、直方图、热力图 | ✅ |
| 8 | 7.21 | Pandas 入门 + PyTorch 起步（Tensor、自动求导、线性回归） | ✅ |
| 9 | 7.22 | 桌面整理 + C盘迁移 + 沟通契约对齐 | ✅ |
| 10 | 7.22 | CNN 手写数字分类（Conv2d、MaxPool2d、调参实验） | ✅ |
| 11 | 7.22 | 数据增强（RandomRotation/RandomAffine、scale最佳范围） | ✅ |
| 12 | 7.23 | 猫狗分类 — 迁移学习（ResNet18、特征提取→微调） | ✅ |
| 13 | 7.23 | NLP 文本分类入门（ag_news、Embedding、LSTM、BiLSTM） | ✅ |

## 仓库结构

```
├── week1-python/          # Python 基础练习
├── week2-pytorch/         # PyTorch 练习（待整理）
├── week3-paper/           # 论文阅读笔记
├── code/                  # 按天分类的代码
│   ├── day6/  day8/  day9/  day10/
├── pytorch/               # PyTorch 完整代码
│   ├── mnist_train.py     # Linear 模型
│   ├── mnist_cnn.py       # CNN 模型（99.19%）
│   ├── day11_augmentation.py  # 数据增强
│   ├── cats_vs_dogs.py    # 迁移学习猫狗分类（98.76%）
│   └── text_classifier.py # NLP 文本分类（ag_news 91%）
├── data/                  # 数据集（不追踪）
├── kb-auto.json           # 自动记录的知识库（36条）
├── planner.html           # 学习计划看板
└── start_planner.bat      # 计划启动器
```

## 实验数据

| 模型 | 任务 | 测试集准确率 |
|------|------|-------------|
| Linear (784→128→10) | MNIST | 97.16% |
| CNN (32通道, 3×3) | MNIST | 98.65% |
| CNN (64通道, 3×3) | MNIST | 98.97% |
| CNN (32通道, 5×5) | MNIST | 99.19% |
| CNN + 数据增强 | MNIST | 99.26% |
| ResNet18 特征提取 | 猫狗分类 | 98.27% |
| ResNet18 微调 | 猫狗分类 | 98.76% |
| Embedding + 平均池化 | ag_news (4类) | 84.84% |
| BiLSTM (12万数据) | ag_news (4类) | 91.08% |

## GPU

NVIDIA GeForce RTX 5060 Laptop GPU (8GB), CUDA 13.2, PyTorch 2.13+cu132

---

## 关于我

南京邮电大学 人工智能学院 2025级本科生
