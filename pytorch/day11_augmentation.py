"""Day 11 — 数据增强 (Data Augmentation)
先看增强效果，再改进 CNN"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================
# 1. 什么是数据增强？
# ============================
# 数据增强 = 对原始图片做微小变换（旋转/平移/缩放等），
# 生成"新"图片，但标签不变。
#
# 比如数字"5"转一点点、拉宽一点、模糊一点——还是5。
# 模型看到更多样子的5，就不会死记硬背，泛化能力更强。
#
# 关键原则：变换不能改变语义（7翻转还是7，6翻转就变9了！）

# ============================
# 2. 看几种增强效果
# ============================
orig_set = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=None)

# 定义几种不同的增强方式
augmentations = {
    "原图": transforms.Compose([
        transforms.ToTensor(),
    ]),
    "随机旋转 ±30°": transforms.Compose([
        transforms.RandomRotation(30),
        transforms.ToTensor(),
    ]),
    "随机平移 ±20%": transforms.Compose([
        transforms.RandomAffine(degrees=0, translate=(0.2, 0.2)),
        transforms.ToTensor(),
    ]),
    "缩放 ±30%": transforms.Compose([
        transforms.RandomAffine(degrees=0, scale=(0.5, 1.5)),
        transforms.ToTensor(),
    ]),
    "组合：旋转+平移+缩放": transforms.Compose([
        transforms.RandomRotation(15),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.5, 1.5
                                                                        )),
        transforms.ToTensor(),
    ]),
}

# 取一张原图展示不同增强效果
img, label = orig_set[0]  # 拿第一张图

fig, axes = plt.subplots(2, 5, figsize=(12, 5))
axes = axes.flatten()

for idx, (name, aug) in enumerate(augmentations.items()):
    # 对同一张图做多次增强，每次都不同
    aug_img = aug(img)  # 这里 aug 接受的是 PIL Image
    axes[idx].imshow(aug_img.squeeze(), cmap='gray')
    axes[idx].set_title(name)
    axes[idx].axis('off')

# 再展示一批增强后的多样性
for idx in range(5, 10):
    aug_img = augmentations["组合：旋转+平移+缩放"](img)
    axes[idx].imshow(aug_img.squeeze(), cmap='gray')
    axes[idx].set_title(f"组合变体 {idx-4}")
    axes[idx].axis('off')

plt.tight_layout()
plt.savefig("augmentation_samples.png")
plt.close()
print("增强效果图已保存: augmentation_samples.png\n")


# ============================
# 3. 用增强数据训练 CNN
# ============================
# 关键区分：
#   - 训练集：用增强，让模型看到更多变体
#   - 测试集：不用增强，保持原始数据公平评估

# 训练集增强
train_transform = transforms.Compose([
    transforms.RandomRotation(15),           # 随机旋转 ±15°
    transforms.RandomAffine(                  # 随机平移+缩放
        degrees=0, translate=(0.1, 0.1), scale=(0.5, 1.5)
    ),
    transforms.ToTensor(),
])

# 测试集不变
test_transform = transforms.ToTensor()

trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=train_transform)
testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=test_transform)

trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)


# ============================
# 4. 同样结构的 CNN
# ============================
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 64, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 64, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 5 * 5, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(-1, 64 * 5 * 5)
        x = self.classifier(x)
        return x


model = CNN()
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

loss_history = []
acc_history = []

print("开始训练（带数据增强）...")
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
    print(f"第{epoch+1}轮  loss: {avg_loss:.4f}  准确率: {accuracy:.2f}%")


# ============================
# 5. 测试集评估
# ============================
correct = 0
total = 0
with torch.no_grad():
    for images, labels in testloader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
test_acc = 100 * correct / total
print(f"\n测试集准确率: {test_acc:.2f}%")


# ============================
# 6. loss/准确率曲线
# ============================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
ax1.plot(loss_history)
ax1.set_title("Loss（越低越好）")
ax1.set_xlabel("训练轮次")
ax1.set_ylabel("损失值")
ax2.plot(acc_history)
ax2.set_title("训练集准确率（越高越好）")
ax2.set_xlabel("训练轮次")
ax2.set_ylabel("准确率(%)")
plt.tight_layout()
plt.savefig("aug_training_history.png")
plt.close()

print("\n===== 小结 =====")
print("1. 数据增强 = 对训练图片做随机变换，变出更多训练数据")
print("2. 训练集用增强，测试集不用 —— 保证测试公平")
print("3. 常见方式：旋转、平移、缩放、翻转、加噪声")
print("4. 原则：变换不能改变图片含义（MNIST 里 6 翻转就变 9 了）")
print(f"5. 本模型测试准确率: {test_acc:.2f}%")
