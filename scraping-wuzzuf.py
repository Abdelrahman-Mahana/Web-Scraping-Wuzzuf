from bs4 import BeautifulSoup
import requests
import csv
import itertools
import pandas as pd
num_pages = 0

Name_Job = []
Name_Company = []
Type_Job = []
Locatin = []
Time_Post = []
Experienced = []
Links = []


while True:
    page = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=data%20analysis&start={num_pages}")
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    page_limit = int(soup.find('strong').text.strip())  
    if(num_pages > page_limit // 15):
        print('done')
        break

    def get_data (page):
        #get job name
        jobs_name = soup.find_all('h2', {'class': 'css-m604qf'})
        for job in jobs_name:
            name = job.text.strip()
            Name_Job.append(name)
            link = job.find('a').get('href')
            Links.append(link)
        
            
        #get company name
        companies_name = soup.find_all('div', {'class': 'css-d7j1kk'})
        for company in companies_name:
            Name_Company.append(company.find('a').text.strip().replace('-', ''))
            
        #get job type
        jobs_type = soup.find_all('a', {'class': 'css-n2jc4m'})
        for job_type in jobs_type:
            Type_Job.append(job_type.find('span').text.strip())
            
        #get location
        locations = soup.find_all('div', {'class': 'css-d7j1kk'})
        for location in locations:
            Locatin.append(location.find('span').text.strip().replace(',', '-'))
            
        #get time post
        new_time_post = soup.find_all('div', {'class': 'css-4c4ojb'})
        old_time_post = soup.find_all('div', {'class': 'css-do6t5g'})
        time_post = [*new_time_post, *old_time_post]
        for time in time_post:
            Time_Post.append(time.text.strip())
            
        #get experienced
        experienced = soup.find_all('div', {'class': 'css-y4udm8'})
        for exp in experienced:
            Experienced.append(exp.find_all('div')[1].text.strip())
        

    get_data(page)
    num_pages += 1
    print(f'page {num_pages} done')
#save data in csv file
result = itertools.zip_longest(Name_Job, Name_Company, Type_Job, Locatin, Time_Post, Experienced, Links)
df = pd.DataFrame(result, columns=['Name_Job', 'Name_Company', 'Type_Job', 'Locatin', 'Time_Post', 'Experienced', 'Links'])
df.to_csv('data.csv', index=False, encoding='utf-8')

