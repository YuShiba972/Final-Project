from PIL import Image, ImageFilter

image = Image.open("满电节点.png")

# 获取图像中每个像素点的RGB值
pixels = image.load()
width, height = image.size

# 将红色元素转换为黑色元素
for i in range(width):
    for j in range(height):
        r, g, b = pixels[i, j]

        # 如果当前像素的红色分量比绿色分量和蓝色分量都高，说明该像素为红色元素
        if r > g and r > b:
            # 把该像素的红色分量改为0，绿色分量改为0，蓝色分量改为0
            pixels[i, j] = (0, 0, 0)

# 使用高斯模糊滤镜处理图像，使得黑色元素的边界更加平滑
image = image.filter(ImageFilter.GaussianBlur(radius=2))

# 将黑色元素转换为绿色元素
for i in range(width):
    for j in range(height):
        if pixels[i, j] == (0, 0, 0):
            pixels[i, j] = (0, 255, 0)

# 保存修改后的图像
image.save("绿色满电.png")
