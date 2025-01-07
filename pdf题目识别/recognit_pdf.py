from pdf2image import convert_from_path
from pytesseract import image_to_string
import re
import os


def extract_questions_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    questions = []

    for i, page in enumerate(pages):
        # 保存每一页为图片
        image_path = f"page_{i + 1}.jpg"
        page.save(image_path, "JPEG")

        # Step 2: 使用 OCR 提取文字
        text = image_to_string(image_path, lang="chi_sim+eng")  # 支持中英混合
        os.remove(image_path)  # 删除临时图片文件

        # Step 3: 使用正则表达式提取题目
        # 假设题目格式为：数字+标点（.、)、、】等）开头
        pattern = r'^\d+[\.\)]\s?.*'  # 根据实际题目格式调整正则表达式
        matches = re.findall(pattern, text, re.MULTILINE)
        questions.extend(matches)

    with open('questions.txt', "w", encoding="utf-8") as f:
        f.write("\n".join(questions))
    print("题目提取成功")


extract_questions_from_pdf("题目pdf/170363485-计算机组成原理 课程设计报告.pdf")
