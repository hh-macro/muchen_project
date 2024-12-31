import os


def count_files(folder_path):

    file_count = sum(os.path.isfile(os.path.join(folder_path, f)) for f in os.listdir(folder_path))
    return file_count


# folder_path = '合格图片'
folder_path = '人物'
print(f"文件夹--'{folder_path}' 中的文件数量为---{count_files(folder_path)}")
