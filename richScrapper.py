# Web scraper of richest men in the world from https://www.forbes.com/real-time-billionaires
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import winsound

def scroll_until_find_class(driver, class_name):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(2)
        
        # Check if the desired element is present
        if len(driver.find_elements(By.CLASS_NAME, class_name)) > 0:
            print(f"Found the element with class {class_name}")
            break
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page but did not find the element")
            break
        last_height = new_height

def scrollToEnd(driver):
    item = driver.find_element(By.CLASS_NAME, "scrolly-table")
    last_height = driver.execute_script("return arguments[0].scrollHeight", item)

    while True:
        # Scroll down within the table element
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", item)

        # Wait to load the page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return arguments[0].scrollHeight", item)
        if new_height == last_height:
            break
        last_height = new_height

# Chrome headless
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

# Load the webpage
driver.get('https://www.forbes.com/real-time-billionaires')

# Wait for the page to load fully
driver.implicitly_wait(10)
print("Page loaded")

scroll_until_find_class(driver, "scrolly-table")
print("Found the table")
# Scroll to the end of the table to load all content
scrollToEnd(driver)
print("Scrolled to the end of the table")

# Get the page source after scrolling
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

# Lists to hold the scraped data
names = []
ranks = []
netWorths = []
sources = []

# Find all 'td' elements with the class 'name'
for element in soup.find_all('td', attrs={'class': 'name'}):
    # Find the 'a' tag within the 'td' element
    name_tag = element.find('a')
    if name_tag:
        names.append(name_tag.text.strip())

for element in soup.find_all('td', attrs={'class': 'rank'}):
    rank = element.find('span')
    if rank:
        ranks.append(rank.text.strip())

for element in soup.find_all('td', attrs={'class':'Net Worth'}):
    netWorth = element.find('span')
    if netWorth:
        netWorths.append(netWorth.text.strip())

for element in soup.find_all('td', attrs={'class':'source'}):
    source = element.find('span')
    if source:
        sources.append(source.text.strip())


# Close the WebDriver
driver.quit()

winsound.PlaySound('C:/Users/munaa/Downloads/mixkit-confirmation-tone-2867.wav', winsound.SND_FILENAME)

# Create a DataFrame from the scraped data
df = pd.DataFrame({
    'Rank': ranks,
    'Name': names,
    'Net Worth': netWorths,
    'Source': sources
})

# Save the DataFrame to a CSV file
df.to_csv("Rich_List.csv", index=False, encoding='utf-8')

# Print the DataFrame
print(df.info())
