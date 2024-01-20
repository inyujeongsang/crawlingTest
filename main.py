 #Python, Selenium, BeautifulSoup을 사용하여 웹페이지를 크롤링한다.
#Selenium은 웹 브라우저를 자동화하는 도구
#BeautifulSoup은 HTML과 XML파일에서 데이터를 추출하기 위한 라이브러리

from selenium.webdriver.chrome.options import Options #Selenium에서 브라우저 옵션을 가져온다.
from selenium.webdriver.common.by import By  #웹요소를 찾기 위한 모듈을 가져온다.
from selenium import webdriver # 라이브러리의 웹드라이버 모듈을 가져온다.
from bs4 import BeautifulSoup

class BrowserManager:
    def __init__(self, url): 
        self.url = url
        pass

    def open_url(self, headless=True, no_sandbox=True) -> str:
        """
        * input
        - boolean headless ...
        - boolean no_sandbox: ...
        --------------------
        * output
        - str: page of url
        """
        chrome_options = Options() #크롬 브라우저 옵션을 설정하는 객체 생성
        if headless:   #브라우저 UI없이 백그라운드에서 실행
            chrome_options.add_argument('--headless')
        if no_sandbox: #**보안제한을 비활성화한다.
            chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('detach', True) #브라우저를 바로 닫지 않고 실행을 유지한다.
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #콘솔 로깅을 비활성화한다.

        driver = webdriver.Chrome(options=chrome_options) #Chrome의 웹드라이버를 초기화한다.
        driver.get(self.url) #지정된 URL로 이동한다.
        handles = driver.window_handles # 현재 열려있는 모든 브라우저 탭의 고유 식별자를 가져온다.
        for handle in handles:
            if handle != handles[0]:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(handles[0])
        page_source = driver.page_source   # 현재 페이지의 HTML 소스를 가져온다.
        driver.close()

        return page_source # 페이지 소스를 반환한다.

from email.parser import Parser
class IncruitParser(Parser): #Parser를 상속받는 IncruitParser 클래스를 만든다.
    def __init__(self):  #아무 작업도 수행하지 않는 생성자 함수
        pass

    @staticmethod  #정적메서드로 정의한다. --> 클래스 인스턴스 없이 호출할 수 있다.
    def parse(source_page: str): #HTML 소스를 파싱하는 메서드 정의
        soup = BeautifulSoup(source_page, 'html.parser')  #HTML소스 파싱

        # Find all job listings
        job_list_container = soup.find('div', class_='tplList tplJobList')

        # print(job_listings)

        jobs = []
        if job_list_container:
            job_listings = job_list_container.find_all('tr', class_='devloopArea')

            for job in job_listings:
                company = job.find('td', class_='tplCo')
                title = job.find('div', class_='titBx')
                details = job.find('p', class_='etc')
                description = job.find('p', class_='dsc')

                # Check if 'title' attribute exists in 'a' tag within the title tag
                if title and title.find('a') and 'title' in title.find('a').attrs:
                    company_name = company.find('a').text.strip() if company and company.find('a') else "N/A"
                    job_title = title.find('a')['title'].strip()

                    if details:
                        detail_items = details.find_all('span', class_='cell')
                        requirements = [item.text.strip() for item in detail_items]
                    else:
                        requirements = []

                    job_description = description.text.strip() if description else "N/A"

                    # Add to jobs list
                    jobs.append({
                        'Company Name': company_name,
                        'Job Title': job_title,
                        'Requirements': requirements,
                        'Description': job_description
                    })

        # Print the parsed data
        for job in jobs:
            print(f"Company: {job['Company Name']}")
            print(f"Title: {job['Job Title']}")
            print(f"Requirements: {', '.join(job['Requirements'])}")
            print(f"Description: {job['Description']}\n\n")

url = 'https://www.jobkorea.co.kr/recruit/joblist?menucode=duty' #크롤링할 웹 페이지의 URL
browser = BrowserManager(url) # URL을 사용하여 BrowserManager객체를 생성한다.
page_source = browser.open_url(True, True) #BrowserManager에 있는 open_url를 호출하여 페이지 소스 가져옴. 
IncruitParser.parse(page_source) #가져온 페이지 소스들을 파싱한다.







