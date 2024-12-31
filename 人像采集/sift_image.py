from PIL import Image, UnidentifiedImageError
import os
import shutil


def imge_page(source_folder, target_folder):
    n = 0
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg')):
            file_path = os.path.join(source_folder, filename)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if (width > 1920 and height > 1080) or (width > 1080 and height > 1920):
                        n += 1
                        img.close()
                        # print(f"图片 {filename} 的大小为 {width}x{height}，大于1920x1080，正在移动...")
                        target_path = os.path.join(target_folder, filename)
                        shutil.move(file_path, target_path)
                        print(f"图片 {filename} 已移动到 {target_folder}, 合格数量---{n}")
                    else:
                        print('', end='')
            except (IOError, ValueError, UnidentifiedImageError) as e:
                print(f"无法处理图片文件 {filename}: {e}")


if __name__ == '__main__':
    source_folder = '人物'
    target_folder = '合格图片'
    imge_page(source_folder, target_folder)
