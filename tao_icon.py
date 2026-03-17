# File: tao_icon.py
from PIL import Image, ImageDraw

# Tạo một hình vuông màu xanh lá (biểu tượng tiền)
img = Image.new('RGB', (64, 64), color = (46, 204, 113))
d = ImageDraw.Draw(img)
d.text((20,15), "$", fill=(255,255,255)) # Vẽ dấu đô la đơn giản

img.save('icon.ico')
print("Đã tạo file icon.ico thành công!")