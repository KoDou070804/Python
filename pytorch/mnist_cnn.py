"""CNN 手写数字识别"""
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================
# 数据准备（和之前一样）
# ============================
transform = transforms.ToTensor()
trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)


# ============================
# CNN 模型
# ============================
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_layers = nn.Sequential(
            # 第1层：卷积 + 池化
            nn.Conv2d(1, 64, 3),   # 输入1通道 → 输出32通道，3×3卷积核
            nn.ReLU(),
            nn.MaxPool2d(2),       # 28×28 → 13×13（池化减半...差不多）

            # 第2层：再卷积 + 池化
            nn.Conv2d(64, 64, 3),  # 32通道 → 64通道
            nn.ReLU(),
            nn.MaxPool2d(2),       # 13×13 → 5×5
        )

        # 全连接层：判断最终结果
        self.classifier = nn.Sequential(
            nn.Linear(64 * 5 * 5, 128),   # 64张5×5特征图 → 128个特征
            nn.ReLU(),
            nn.Linear(128, 10),            # 128个特征 → 10个数字
        )

    def forward(self, x):
        x = self.conv_layers(x)      # 卷积层提取特征
        x = x.view(-1, 64 * 5 * 5)   # 展平：64×5×5 → 1600
        x = self.classifier(x)       # 全连接层分类
        return x


# ============================
# 训练
# ============================
model = CNN()
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

loss_history = []
acc_history = []

for epoch in range(5):
    total_loss = 0
    correct = 0
    total = 0
    for images, labels in trainloader:
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    avg_loss = total_loss / len(trainloader)
    accuracy = 100 * correct / total
    loss_history.append(avg_loss)
    acc_history.append(accuracy)
    print(f"第{epoch+1}轮  loss：{avg_loss:.4f}  准确率：{accuracy:.2f}%")


# ============================
# 画图 + 测试
# ============================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
ax1.plot(loss_history)
ax1.set_title("Loss — 越低越好")
ax1.set_xlabel("训练轮次")
ax1.set_ylabel("损失值")
ax2.plot(acc_history)
ax2.set_title("准确率 — 越高越好")
ax2.set_xlabel("训练轮次")
ax2.set_ylabel("准确率(%)")
plt.tight_layout()
plt.savefig("cnn_training.png")
plt.close()

correct = 0
total = 0
with torch.no_grad():
    for images, labels in testloader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f"\n测试集准确率：{100 * correct / total:.2f}%")
