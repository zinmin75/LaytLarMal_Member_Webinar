from bs4 import BeautifulSoup
import csv

with open('simple.html') as html_file:
    soup = BeautifulSoup(html_file, 'html.parser')

# print(soup.prettify())

# match = soup.title.text
# print(match)

with open('cms_scrape.csv', 'a', encoding='utf-8') as f:
    for article in soup.find_all('div', class_='article'):
        headline = article.h2.a.text.strip()
        summary = article.p.text.strip()

        print(f"{headline},{summary}\n")
        f.write(f"{headline},{summary}\n")