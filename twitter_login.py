import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = 'https://twitter.com/'
YOUR_LOGIN = ''
YOUR_PASS = ''

options = Options()
options.add_argument('--headless=new')
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

# logining on Twitter
login = driver.find_element(by=By.XPATH, value='//a[@href="/login"]')
login.click()
time.sleep(2)

username = driver.find_element(by=By.XPATH, value='//input[@autocomplete="username"]')
username.send_keys(YOUR_LOGIN)

next_button = driver.find_element(by=By.XPATH, value='//span[text()="Next"]')
next_button.click()
time.sleep(2)

password = driver.find_element(by=By.XPATH, value='//input[@autocomplete="current-password"]')
password.send_keys(YOUR_PASS)

login_button = driver.find_element(by=By.XPATH, value='//span[text()="Log in"]')
login_button.click()


# finding all tweets on page
def get_tweet(element):
    try:
        user = element.find_element(By.XPATH, value='.//span[contains(text(), "@")]').text
        text = element.find_element(By.XPATH, value='.//div[@lang]').text
        text = ' '.join(text.split())
    except:
        user, text = '', ''
    return user, text


users, texts = [], []
tweets = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//article[@role="article"]')
            )
        )
# tweets = driver.find_elements(By.XPATH, value='//article[@role="article"]')
for tweet in tweets:
    user, text = get_tweet(tweet)
    users.append(user), texts.append(text)

driver.quit()

df = pd.DataFrame({
    'user': users,
    'text': texts,
})

df.to_csv('tweets.csv', index=False, encoding='utf-8')
