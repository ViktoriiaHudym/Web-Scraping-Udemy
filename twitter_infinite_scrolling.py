import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = 'https://twitter.com/Support'

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


def get_tweet(element):
    try:
        user = element.find_element(By.XPATH, value='.//span[contains(text(), "@")]').text
        text = element.find_element(By.XPATH, value='.//div[@lang]').text
        text = ' '.join(text.split())
    except:
        user, text = '', ''
    return user, text


users, texts = [], []
tweets_ids = set()

scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//article[@role="article"]')
        )
    )
    # tweets = driver.find_elements(By.XPATH, value='//article[@role="article"]')
    for tweet in tweets[-15:]:
        user, text = get_tweet(tweet)
        tweet_id = ''.join([user, text])
        if tweet_id not in tweets_ids:
            tweets_ids.add(tweet_id)
            users.append(user), texts.append(text)

    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        # if new_height == last_height:
        #     scrolling = False
        #     break
        if len(users) > 100:
            scrolling = False
            break
        else:
            last_height = new_height
            break

driver.quit()

df = pd.DataFrame({
    'user': users,
    'text': texts,
})

df.to_csv('tweets_infinite.csv', index=False, encoding='utf-8')
