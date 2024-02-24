import matplotlib.pyplot as plt

# 读取已保存的SVG文件
svg_file = "Figure_1.svg"
img = plt.imread(svg_file)

# 显示SVG图像
plt.imshow(img)
plt.axis('off')  # 可以选择关闭坐标轴
plt.show()
