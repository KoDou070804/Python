

"""项目1：猫狗分类 (Cats vs Dogs) — 迁移学习入门"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================
# 1. 数据集路径
# ============================
data_dir = './cats_vs_dogs'
if not os.path.exists(data_dir):
    print(f"错误：找不到数据目录 {data_dir}")
    print("请确保 cats_vs_dogs/train/cats/ 等目录存在")
    exit()

# ============================
# 2. 查看数据集
# ============================
train_path = os.path.join(data_dir, 'train')
val_path   = os.path.join(data_dir, 'val')
print(f"训练集: {len(os.listdir(os.path.join(train_path, 'cats')))} 猫, "
      f"{len(os.listdir(os.path.join(train_path, 'dogs')))} 狗")
print(f"验证集: {len(os.listdir(os.path.join(val_path, 'cats')))} 猫, "
      f"{len(os.listdir(os.path.join(val_path, 'dogs')))} 狗")

# ============================
# 3. 数据预处理
# ============================
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

train_set = ImageFolder(train_path, transform=train_transform)
val_set   = ImageFolder(val_path,   transform=val_transform)

train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_set,   batch_size=32, shuffle=False)

print(f"类别: {train_set.classes}")

# ============================
# 4. 展示增强后的图
# ============================
images, labels = next(iter(train_loader))
fig, axes = plt.subplots(1, 6, figsize=(12, 3))
for i in range(6):
    img = images[i].permute(1, 2, 0).numpy()
    img = img * np.array(IMAGENET_STD) + np.array(IMAGENET_MEAN)
    img = np.clip(img, 0, 1)
    axes[i].imshow(img)
    axes[i].set_title(train_set.classes[labels[i]])
    axes[i].axis('off')
plt.tight_layout()
plt.savefig("cats_dogs_samples.png")
plt.close()
print("样本图已保存: cats_dogs_samples.png\n")

# ============================
# 5. 迁移学习：加载预训练 ResNet18
# ============================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.DEFAULT)

in_features = model.fc.in_features
model.fc = nn.Linear(in_features, 2)
model = model.to(device)

# 冻结所有层，只训练最后一层
for param in model.parameters():
    param.requires_grad = False
for param in model.fc.parameters():
    param.requires_grad = True

print("修改后的最后一层:", model.fc)

# ============================
# 6. 训练
# ============================
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

num_epochs = 10
train_loss_history = []
val_acc_history = []

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    train_loss_history.append(avg_loss)

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    acc = 100 * correct / total
    val_acc_history.append(acc)
    print(f"第{epoch+1}轮  loss: {avg_loss:.4f}  验证准确率: {acc:.2f}%")

# ============================
# 7. 微调 (Fine-tuning)
# ============================
# 只训练最后一层，前面卷积层冻结住了。
# 现在解冻最后几层一起训练，让它们也适应猫狗任务
print("\n===== 第二阶段：解冻 layer4 + fc，继续微调 =====")

# 解冻最后几层
for param in model.layer4.parameters():
    param.requires_grad = True
for param in model.fc.parameters():
    param.requires_grad = True

# 微调要用更小的学习率（已经在好的位置上了，不能调太猛）
optimizer_ft = optim.Adam([
    {'params': model.layer4.parameters(), 'lr': 0.0001},
    {'params': model.fc.parameters(), 'lr': 0.0001},
])

for epoch in range(5):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        optimizer_ft.zero_grad()
        loss.backward()
        optimizer_ft.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    train_loss_history.append(avg_loss)

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    acc = 100 * correct / total
    val_acc_history.append(acc)
    print(f"[微调] 第{epoch+1}轮  loss: {avg_loss:.4f}  验证准确率: {acc:.2f}%")

# ============================
# 8. 画图
# ============================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
ax1.plot(train_loss_history)
ax1.set_title("Loss")
ax1.set_xlabel("训练轮次")
ax1.set_ylabel("损失值")
ax2.plot(val_acc_history)
ax2.set_title("验证集准确率")
ax2.set_xlabel("训练轮次")
ax2.set_ylabel("准确率(%)")
plt.tight_layout()
plt.savefig("cats_dogs_training.png")
plt.close()
print("训练曲线已保存: cats_dogs_training.png")

# ============================
# 9. 看预测结果
# ============================
model.eval()
images, labels = next(iter(val_loader))
images, labels = images.to(device), labels.to(device)
outputs = model(images)
_, predicted = torch.max(outputs, 1)

fig, axes = plt.subplots(2, 5, figsize=(12, 5))
axes = axes.flatten()
for i in range(10):
    img = images[i].cpu().permute(1, 2, 0).numpy()
    img = img * np.array(IMAGENET_STD) + np.array(IMAGENET_MEAN)
    img = np.clip(img, 0, 1)
    axes[i].imshow(img)
    gt = val_set.classes[labels[i]]
    pred = val_set.classes[predicted[i]]
    color = 'green' if gt == pred else 'red'
    axes[i].set_title(f"真: {gt} / 预: {pred}", color=color)
    axes[i].axis('off')
plt.tight_layout()
plt.savefig("cats_dogs_prediction.png")
plt.close()
print("预测结果图已保存: cats_dogs_prediction.png")
