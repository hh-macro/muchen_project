import requests
# https://stock.tuchong.com/search?page=1&sort=0&source=tc_pc_home_search&term=%E4%BA%BA%E5%83%8F
# https://www.gettyimages.com/search/2/image?phrase=people
# https://stock.adobe.com/search/images?k=people&search_type=usertyped&asset_id=203895572
# https://www.pexels.com/search/people/   111
# 图片的 URL
image_url = 'https://cdn9-banquan.ituchong.com/weili/image/ml/1927097623355457539.webp'

response = requests.get(image_url)

image_binary = response.content

with open('output_file.jpg', 'wb') as file:
    file.write(image_binary)
print('图片已保存为 JPG 文件。')
