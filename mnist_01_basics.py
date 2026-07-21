"""MNIST 手写数字识别 — 第1步：数据加载与探索"""
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# ============================
# 1. 下载 MNIST 数据集
# ============================
# transforms.ToTensor() 把 PIL图片/NumPy数组 → Tensor，并自动归一化到 [0,1]
transform = transforms.ToTensor()

# 训练集: download=True 第一次会自动下载
trainset = torchvision.datasets.MNIST(
    root='./data', train=True, download=True, transform=transform)
# 测试集
testset = torchvision.datasets.MNIST(
    root='./data', train=False, download=True, transform=transform)

print(f"训练集大小: {len(trainset)}")
print(f"测试集大小: {len(testset)}")
print(f"图片形状: {trainset[0][0].shape}")  # [1, 28, 28] = 通道数, 高, 宽
print(f"标签范围: 0-{trainset.classes[-1]}")

# ============================
# 2. 查看几张图片
# ============================
fig, axes = plt.subplots(1, 6, figsize=(10, 3))
for i in range(6):
    img, label = trainset[i]
    axes[i].imshow(img.squeeze(), cmap='gray')  # squeeze() 去掉通道维度 (1,28,28)→(28,28)
    axes[i].set_title(f"标签: {label}")
    axes[i].axis('off')
plt.tight_layout()
plt.savefig('mnist_samples.png')
print("\n图片已保存: mnist_samples.png")

# ============================
# 3. DataLoader: 批量加载数据
# ============================
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=64, shuffle=True)
testloader = torch.utils.data.DataLoader(
    testset, batch_size=64, shuffle=False)

# 验证一个批次
images, labels = next(iter(trainloader))
print(f"\n一个批次形状: images {images.shape}, labels {labels.shape}")
# images.shape = [64, 1, 28, 28], labels.shape = [64]
