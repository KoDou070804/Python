"""项目2 — NLP文本分类入门 (使用 ag_news 数据集)
核心：文本 → 数字 → 神经网络"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from collections import Counter
import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# ============================
# 1. 下载数据集
# ============================
from datasets import load_dataset
print("下载 ag_news 数据集...")
dataset = load_dataset('fancyzhx/ag_news')
print(f"训练集: {len(dataset['train'])} 条")
print(f"测试集: {len(dataset['test'])} 条")
print(f"类别: {dataset['train'].features['label'].names}")
# ['World', 'Sports', 'Business', 'Sci/Tech']

train_texts = dataset['train']['text'][:20000]   # 取前 20000 条，先跑快点
train_labels = dataset['train']['label'][:20000]
test_texts = dataset['test']['text']
test_labels = dataset['test']['label']


# ============================
# 2. 文本 → 数字
# ============================
# 核心问题：神经网络只能处理数字，不能处理文字
# 解决思路：
#   1. 分词（Tokenization）：把句子拆成单词
#   2. 建词表（Vocabulary）：给每个单词一个编号
#   3. 句子 → 编号序列
#   4. 补齐到等长（Padding）

def tokenize(text):
    """简单的分词：转小写，按空格/标点拆分"""
    import re
    text = text.lower()
    return re.findall(r'\w+', text)  # 只保留字母数字

# 构建词表
counter = Counter()
for text in train_texts:
    counter.update(tokenize(text))

# 保留最常见的 20000 个词
vocab_size = 20000
most_common = counter.most_common(vocab_size - 2)  # -2 留给特殊符号

# 词 → 编号 的映射表
word2idx = {'<PAD>': 0, '<UNK>': 1}  # PAD=填充, UNK=未知词
for word, _ in most_common:
    word2idx[word] = len(word2idx)

idx2word = {v: k for k, v in word2idx.items()}
print(f"\n词表大小: {len(word2idx)}")
print(f"前10个词: {list(word2idx.keys())[:10]}")

def encode(text, max_len=64):
    """把一段文本变成固定长度的数字序列"""
    tokens = tokenize(text)
    ids = [word2idx.get(t, word2idx['<UNK>']) for t in tokens]
    # 截断或填充到 max_len
    if len(ids) > max_len:
        ids = ids[:max_len]
    else:
        ids = ids + [word2idx['<PAD>']] * (max_len - len(ids))
    return ids

# 展示编码过程
print("\n编码示例:")
print(f"原文: {train_texts[0][:80]}...")
print(f"tokens: {tokenize(train_texts[0])[:10]}")
print(f"编码: {encode(train_texts[0])[:15]}...")


# ============================
# 3. DataLoader
# ============================
class TextDataset(Dataset):
    def __init__(self, texts, labels, max_len=64):
        self.data = [encode(t, max_len) for t in texts]
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return torch.tensor(self.data[idx], dtype=torch.long), \
               torch.tensor(self.labels[idx], dtype=torch.long)

max_len = 64
batch_size = 128

train_set = TextDataset(train_texts, train_labels, max_len)
test_set  = TextDataset(test_texts, test_labels, max_len)

train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
test_loader  = DataLoader(test_set, batch_size=batch_size)

print(f"\n一个批次形状: {next(iter(train_loader))[0].shape}")
# [128, 64] = [batch_size, max_len]


# ============================
# 4. 模型：词嵌入 + 平均池化 + 分类
# ============================
# Embedding 层是 NLP 版的 "卷积层"：
#   卷积层：把像素值映射成有意义的特征
#   嵌入层：把词编号映射成有意义的词向量
#
# 原理：每个词用一个稠密向量表示（如 100 维），
#       相似的词（cat/dog）在向量空间里靠得近
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=100, num_classes=4):
        super().__init__()
        # 嵌入层：词编号 → 稠密向量
        # 就像一个可学习的查找表
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        # 分类层
        self.fc = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        # x: [batch_size, max_len]
        embed = self.embedding(x)        # [batch, max_len, embed_dim]
        pooled = embed.mean(dim=1)       # [batch, embed_dim]
        out = self.fc(pooled)            # [batch, num_classes]
        return out

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\n使用设备: {device}")

model = TextClassifier(len(word2idx), embed_dim=100, num_classes=4).to(device)
print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")


# ============================
# 5. 训练
# ============================
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 5
train_loss_history = []
train_acc_history = []

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = model(inputs)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    avg_loss = total_loss / len(train_loader)
    accuracy = 100 * correct / total
    train_loss_history.append(avg_loss)
    train_acc_history.append(accuracy)
    print(f"第{epoch+1}轮  loss: {avg_loss:.4f}  准确率: {accuracy:.2f}%")


# ============================
# 6. 测试
# ============================
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_acc = 100 * correct / total
print(f"\n测试集准确率: {test_acc:.2f}%")


# ============================
# 7. 进阶：LSTM 模型
# ============================
# 平均池化的局限：丢失词序
#   "狗追猫" vs "猫追狗" → 平均池化后一样
# LSTM 能按顺序"读"每个词，记住上下文
print("\n" + "="*50)
print("LSTM 模型 — 能捕捉词序")
print("="*50)

class LSTMTextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=100, hidden_dim=128, num_classes=4, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.3,
        )
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        embed = self.embedding(x)
        lstm_out, (h_n, c_n) = self.lstm(embed)
        last_hidden = h_n[-1]
        out = self.fc(last_hidden)
        return out

model_lstm = LSTMTextClassifier(len(word2idx)).to(device)
print(f"LSTM 参数量: {sum(p.numel() for p in model_lstm.parameters()):,}")

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_lstm.parameters(), lr=0.001)

for epoch in range(5):
    model_lstm.train()
    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model_lstm(inputs)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    avg_loss = total_loss / len(train_loader)
    accuracy = 100 * correct / total
    print(f"第{epoch+1}轮  loss: {avg_loss:.4f}  准确率: {accuracy:.2f}%")

# LSTM 测试
model_lstm.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model_lstm(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

lstm_test_acc = 100 * correct / total
print(f"\nLSTM 测试集准确率: {lstm_test_acc:.2f}% (之前平均池化: {test_acc:.2f}%)")


# ============================
# 8. 再进阶：双向 LSTM (BiLSTM)
# ============================
# 单向 LSTM：从前往后读
# 双向 LSTM：从前往后读一遍 + 从后往前读一遍 → 每个词看到完整的上下文
print("\n" + "="*50)
print("BiLSTM 模型 — 双向阅读，理解完整上下文")
print("="*50)

class BiLSTMTextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=100, hidden_dim=128, num_classes=4, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        # bidirectional=True 就是双向 LSTM
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.3,
            bidirectional=True,    # ← 关键：双向
        )
        # 双向 LSTM 输出维度是 hidden_dim * 2（正向 + 反向拼接）
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embed = self.embedding(x)
        lstm_out, (h_n, c_n) = self.lstm(embed)
        # 拼接最后一层的正向和反向输出
        h_forward = h_n[-2]   # 正向最后一层
        h_backward = h_n[-1]  # 反向最后一层
        h_combined = torch.cat([h_forward, h_backward], dim=1)  # [batch, hidden*2]
        out = self.fc(h_combined)
        return out

model_bilstm = BiLSTMTextClassifier(len(word2idx)).to(device)
print(f"BiLSTM 参数量: {sum(p.numel() for p in model_bilstm.parameters()):,}")

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_bilstm.parameters(), lr=0.001)

for epoch in range(5):
    model_bilstm.train()
    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model_bilstm(inputs)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    avg_loss = total_loss / len(train_loader)
    accuracy = 100 * correct / total
    print(f"第{epoch+1}轮  loss: {avg_loss:.4f}  准确率: {accuracy:.2f}%")

# BiLSTM 测试
model_bilstm.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model_bilstm(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

bilstm_test_acc = 100 * correct / total
print(f"\nBiLSTM 测试集准确率: {bilstm_test_acc:.2f}%")
print(f"平均池化: {test_acc:.2f}% | LSTM: {lstm_test_acc:.2f}% | BiLSTM: {bilstm_test_acc:.2f}%")


# ============================
# 9. 实验：用全部 12 万数据训练 BiLSTM
# ============================
# 数据越多，复杂模型越能发挥优势
print("\n" + "="*50)
print("实验：BiLSTM 用全部 12 万条数据训练")
print("="*50)

full_train_texts = dataset['train']['text']
full_train_labels = dataset['train']['label']

full_train_set = TextDataset(full_train_texts, full_train_labels, max_len)
full_train_loader = DataLoader(full_train_set, batch_size=batch_size, shuffle=True)

model_bilstm_full = BiLSTMTextClassifier(len(word2idx)).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_bilstm_full.parameters(), lr=0.001)

for epoch in range(5):
    model_bilstm_full.train()
    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in full_train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model_bilstm_full(inputs)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    avg_loss = total_loss / len(full_train_loader)
    accuracy = 100 * correct / total
    print(f"第{epoch+1}轮  loss: {avg_loss:.4f}  准确率: {accuracy:.2f}%")

model_bilstm_full.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model_bilstm_full(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

full_acc = 100 * correct / total
print(f"\n=== 最终对比 ===")
print(f"平均池化(2万数据):  {test_acc:.2f}%")
print(f"BiLSTM(2万数据):    {bilstm_test_acc:.2f}%")
print(f"BiLSTM(12万数据):   {full_acc:.2f}%")
print(f"提升: +{full_acc - bilstm_test_acc:.2f}%")


# ============================
# 10. 对比预测
# ============================
model.eval()
texts_sample = test_texts[:5]
labels_sample = test_labels[:5]
inputs = torch.tensor([encode(t, max_len) for t in texts_sample]).to(device)
outputs = model(inputs)
_, predicted = torch.max(outputs, 1)

class_names = dataset['train'].features['label'].names
print("\n预测示例:")
for i in range(5):
    print(f"  原文: {texts_sample[i][:60]}...")
    print(f"  真实: {class_names[labels_sample[i]]}  →  预测: {class_names[predicted[i]]}")
    print()
