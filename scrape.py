from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://weworkremotely.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
df = pd.DataFrame(columns=['job_title', 'company', 'description', 'apply', 'tags'])
job_title = []
company = []
job_desc = []
apply_link = []
tags = []
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = soup.find_all('li', class_ = 'feature')
    links = ['https://weworkremotely.com' + job.find_all('a')[1]['href'] for job in jobs]
    for link in links:
        response2 = requests.get(link, headers=headers)
        if response2.status_code == 200:
            soup2 = BeautifulSoup(response2.content, 'html.parser')
            job_title.append(soup2.find('h1').text)
            company.append(soup2.find('h2').text)
            job_desc.append(soup2.find('div', class_='listing-container').text)
            apply_link.append(soup2.find('div', class_='apply_tooltip').find('a')['href'])
            tags_list = soup2.find_all('span', class_='listing-tag')
            tags.append([tag.text for tag in tags_list])
df['job_title'] = job_title
df['company'] = company
df['description'] = job_desc
df['apply'] = apply_link
df['tags'] = tags
df.to_csv('jobs.csv')

