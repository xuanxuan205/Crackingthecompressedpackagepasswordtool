from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建图标目录
    os.makedirs('assets', exist_ok=True)
    
    # 创建一个512x512的图像
    size = 512
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制背景圆形
    circle_color = (41, 128, 185)  # 蓝色
    draw.ellipse([(0, 0), (size, size)], fill=circle_color)
    
    # 绘制锁的图案
    lock_color = (255, 255, 255)  # 白色
    lock_width = size * 0.4
    lock_height = size * 0.5
    lock_x = (size - lock_width) / 2
    lock_y = (size - lock_height) / 2
    
    # 绘制锁体
    draw.rectangle(
        [(lock_x, lock_y), (lock_x + lock_width, lock_y + lock_height)],
        fill=lock_color
    )
    
    # 绘制锁的顶部
    arc_width = lock_width * 0.8
    arc_height = lock_height * 0.3
    arc_x = (size - arc_width) / 2
    arc_y = lock_y - arc_height
    draw.arc(
        [(arc_x, arc_y), (arc_x + arc_width, arc_y + arc_height * 2)],
        0, 180, fill=lock_color, width=int(size * 0.05)
    )
    
    # 保存为ICO文件
    image.save('assets/icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("图标已创建：assets/icon.ico")

if __name__ == '__main__':
    create_icon() 