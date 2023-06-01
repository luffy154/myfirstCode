from bs4 import BeautifulSoup

# 打开 HTML 文件
with open('example.xml', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 创建 BeautifulSoup 对象
soup = BeautifulSoup(html_content, 'html.parser')

# 示例分析：获取标题和所有链接
title = soup.title.text
links = soup.find_all('a')

# 输出结果
print(f"网页标题：{title}")
print("链接列表：")
for link in links:
    print(link.get('href'))
