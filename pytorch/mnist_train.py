"""手写数字识别：完整训练脚本"""
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# 让 matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 第一部分：准备数据
# ============================================

# transform = 数据预处理：把图片转成 Tensor，值从0-255缩到0-1
transform = transforms.ToTensor()

# 下载 MNIST 数据集（训练集6万张，测试集1万张）
trainset = torchvision.datasets.MNIST(
    root='./data', train=True, download=True, transform=transform)
testset = torchvision.datasets.MNIST(
    root='./data', train=False, download=True, transform=transform)

# DataLoader = 数据加载器：把数据分成小包(batch)，每次喂给模型一批
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=64, shuffle=True)
testloader = torch.utils.data.DataLoader(
    testset, batch_size=64, shuffle=False)


# ============================================
# 第二部分：定义模型（神经网络）
# ============================================

class DigitClassifier(nn.Module):
    """手写数字分类器
    结构：输入层(784) → 隐藏层(128) → 输出层(10)
    784 = 28×28 每张图片展开成1维
    10  = 0-9 共10个数字
    """
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 128),   # 第1层：784维 → 128维
            nn.ReLU(),             # 激活函数：把负数变成0，增加表达能力
            nn.Linear(128, 10),    # 第2层：128维 → 10维（10个数字的概率）
        )

    def forward(self, x):
        """forward = 前向传播：输入→计算→输出"""
        x = x.view(-1, 784)    # 展平：把28×28拉成784的一维向量
        x = self.layers(x)     # 经过两层计算
        return x


# ============================================
# 第三部分：训练设置
# ============================================

model = DigitClassifier()
loss_fn = nn.CrossEntropyLoss()   # 交叉熵损失 = 分类任务专用损失
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器

# 记录训练过程的 loss（损失）和 accuracy（准确率）
loss_history = []
acc_history = []


# ============================================
# 第四部分：训练循环
# ============================================

epochs = 5  # epoch = 训练轮次（看完整数据集的次数）

for epoch in range(epochs):
    total_loss = 0
    correct = 0      # 猜对的次数
    total = 0        # 总次数

    for images, labels in trainloader:
        # images: [64, 1, 28, 28] — 64张图，1通道，28×28
        # labels: [64] — 每张图对应的真实数字

        # 1. 用模型猜
        outputs = model(images)        # outputs: [64, 10] — 每张图猜10个数字的概率
        loss = loss_fn(outputs, labels) # 算loss：猜的和真实标签比

        # 2. 反向传播（算梯度+调参数）
        optimizer.zero_grad()  # 清空上次梯度
        loss.backward()        # 算梯度（该往哪调）
        optimizer.step()       # 调参数（实际调一步）

        # 3. 统计
        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)  # 取概率最高的那个数字作为预测结果
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    # 每轮结束算准确率
    avg_loss = total_loss / len(trainloader)
    accuracy = 100 * correct / total
    loss_history.append(avg_loss)
    acc_history.append(accuracy)

    print(f"第{epoch+1}轮  loss：{avg_loss:.4f}  准确率：{accuracy:.2f}%")


# ============================================
# 第五部分：画图展示训练结果
# ============================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))

# loss 曲线（应该越来越低）
ax1.plot(loss_history)
ax1.set_title("Loss（损失）— 越低越好")
ax1.set_xlabel("训练轮次")
ax1.set_ylabel("损失值")

# 准确率曲线（应该越来越高）
ax2.plot(acc_history)
ax2.set_title("Accuracy（准确率）— 越高越好")
ax2.set_xlabel("训练轮次")
ax2.set_ylabel("准确率(%)")

plt.tight_layout()
plt.savefig("training_history.png")
print("训练曲线已保存: training_history.png")


# ============================================
# 第六部分：测试集上评估
# ============================================

correct = 0
total = 0
with torch.no_grad():  # 测试时不需要算梯度，省内存
    for images, labels in testloader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"\n测试集准确率：{100 * correct / total:.2f}%")
