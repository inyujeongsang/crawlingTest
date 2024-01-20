from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class BrowserManager:
    def __init__(self, url):
        self.url = url

    def open_url(self, headless=True, no_sandbox=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        if no_sandbox:
            chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_experimental_option('detach', True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)

        # 페이지 요소와 상호작용
        #wait = WebDriverWait(driver, 10)
        #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='duty_step1_10031']"))).click()
        #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='duty_step2_1000229']"))).click()
        #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='duty_step3_1000229']"))).click()
        #wait.until(EC.element_to_be_clickable((By.ID, "dev-btn-search"))).click()

        # 페이지 로드를 기다린다
        #time.sleep(5)

        # BeautifulSoup로 HTML 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 여기에 필요한 데이터 추출 로직 추가

        # 드라이버 종료
        driver.quit()

        return soup

# 사용 예시
url = "https://www.jobkorea.co.kr/recruit/joblist?menucode=duty"
browser_manager = BrowserManager(url)
page_content = browser_manager.open_url()
# page_content를 이용하여 필요한 데이터 추출
