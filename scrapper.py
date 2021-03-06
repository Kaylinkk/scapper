import requests
from bs4 import BeautifulSoup


def get_last_page(stack_url):
    result = requests.get(stack_url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find('h2').find('a')['title']
    company, location = html.find('h3', {
        "class": "mb4"
    }).find_all("span", recursive=False)  # 첫번째 span만 가져온다
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link:': f'https://stackoverflow.com/jobs/{job_id}'
    }


def extract_jobs(last_page, stack_url):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping stack_overflow: Page : {page}')
        result = requests.get(f'{stack_url}&pg={page+1}')
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all('div', {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
        return jobs


def get_jobs(word):
    stack_url = f"https://stackoverflow.com/jobs?d=20&l=japan&q={word}&u=Km"

    last_page = get_last_page(stack_url)
    jobs = extract_jobs(last_page, stack_url)

    return jobs
