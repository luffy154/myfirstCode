from bs4 import BeautifulSoup

with open('code.xml', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
codeHtml = soup.find_all(name='div', attrs={'class': 'hljs-ln-line'})
for code in codeHtml:
    print(f"{code.get_text()}")
