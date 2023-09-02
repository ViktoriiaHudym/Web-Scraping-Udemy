import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


website = 'https://www.adamchoi.co.uk/overs/detailed'

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager(
            latest_release_url='https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json',
            driver_version='116.0.5845.96'
        ).install()
    ))

driver.get(website)

all_matches_button = driver.find_element(by=By.XPATH, value='//label[@analytics-event="All matches"]')
all_matches_button.click()

dropdown = Select(driver.find_element(by=By.ID, value='country'))
dropdown.select_by_visible_text('Spain')

time.sleep(3)

matches = driver.find_elements(by=By.TAG_NAME, value='tr')

date = []
home_team = []
score = []
away_team = []


for match in matches:
    try:
        away_team.append(match.find_element(by=By.XPATH, value='./td[4]').text)
        date.append(match.find_element(by=By.XPATH, value='./td[1]').text)
        home_team.append(match.find_element(by=By.XPATH, value='./td[2]').text)
        score.append(match.find_element(by=By.XPATH, value='./td[3]').text)
    except:     # sometimes it's not rows with game data but other
        continue

driver.quit()

df = pd.DataFrame({
    'date': date,
    'home_team': home_team,
    'score': score,
    'away_team': away_team
})

df.to_csv('data.csv', index=False)
print(df)


