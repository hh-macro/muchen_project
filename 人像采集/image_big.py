from PIL import Image
import os


def resize_image(source_folder, target_folder, new_width, new_height):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # 支持常见格式
            input_path = os.path.join(source_folder, filename)
            output_path = os.path.join(target_folder, filename)

            with Image.open(input_path) as img:
                # 使用Lanczos插值方法放大图片
                img_resized = img.resize((new_width, new_height), Image.LANCZOS)

                img_resized.save(output_path)
                print(f"图片 {filename} 已放大并保存到 {target_folder}")


# 原始图片文件夹路径
source_folder = '人物'
# 放大后图片保存的文件夹路径
target_folder = 'new_jpg'
# 新的宽度和高度
new_width = 1920
new_height = 1080

resize_image(source_folder, target_folder, new_width, new_height)
