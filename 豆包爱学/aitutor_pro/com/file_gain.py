import ast


def gain():
    file_path = r'E:\AAA-project\muchen_project\豆包爱学\aitutor_pro\utils\detected_filenames.txt'

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    try:
        uuid_list = ast.literal_eval(content)
    except (ValueError, SyntaxError) as e:
        print(f"解析错误: {e}")
    return uuid_list


if __name__ == '__main__':
    print(gain())