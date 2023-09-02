import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = 'https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=1bb99d4d-8ec8-42a3-bb35-704e849c2bc6&pf_rd_r=CD81998AKAQAVTKFVDTT&pageLoadId=uAo6BRwenCkf93bi&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc'

options = Options()
# options.add_argument('--headless=new')
options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager(
            latest_release_url='https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json',
            driver_version='116.0.5845.96'
        ).install()
    ),
    options=options
)

driver.get(website)
# driver.maximize_window()

pagination = driver.find_element(by=By.XPATH, value='//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(by=By.TAG_NAME, value='li')

last_page = int(pages[-2].text)
current_page = 1

titles, authors, lengths = [], [], []
while current_page <= last_page:

    container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'adbl-impression-container ')
        )
    )
    # container = driver.find_element(by=By.CLASS_NAME, value='adbl-impression-container ')
    products = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, './/li[contains(@class, "productListItem")]')
        )
    )
    products = container.find_elements(by=By.XPATH, value='.//li[contains(@class, "productListItem")]')

    for product in products:
        title = product.find_element(by=By.XPATH, value='.//h3[contains(@class, "bc-heading")]').text
        author = product.find_element(by=By.XPATH, value='.//li[contains(@class, "authorLabel")]').text
        runtime = product.find_element(by=By.XPATH, value='.//li[contains(@class, "runtimeLabel")]').text

        titles.append(title)
        authors.append(author)
        lengths.append(runtime)

    current_page += 1

    try:
        next_page = driver.find_element(by=By.XPATH, value='//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df = pd.DataFrame({
    'title': titles,
    'author': authors,
    'runtime': lengths,
})

df.to_csv('books_.csv', index=False)

