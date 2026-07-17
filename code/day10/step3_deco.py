import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)

plt.plot(x, y, 'b-', linewidth=2)
plt.title("正弦曲线")
plt.xlabel("x 值")
plt.ylabel("sin(x)")
plt.xlim(0, 4*np.pi)
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.show()
