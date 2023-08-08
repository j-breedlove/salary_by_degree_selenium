# Required Imports
import csv
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller

# Constants
URL = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'
CSV_FILENAME = 'degree_data.csv'


def initialize_driver():
    """Initialize and return a Chrome webdriver instance."""
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    return driver


def fetch_data_from_url(driver, url=URL):
    """Fetches data from the specified URL using the provided driver."""
    driver.get(url)
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/article/div[2]/table')))
    return table.find_elements(By.TAG_NAME, 'tr')


def write_data_to_csv(rows):
    """Writes the scraped data to a CSV file."""
    with open(CSV_FILENAME, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Degree', 'Early Career Pay', 'Mid-Career Pay'])
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 4:
                degree = re.sub(r'^\d+', '', cells[1].text)
                early_career_pay = cells[3].text.replace('Early Career Pay:\n$', '').replace(',', '')
                mid_career_pay = cells[4].text.replace('Mid-Career Pay:\n$', '').replace(',', '')
                writer.writerow([degree, early_career_pay, mid_career_pay])


def main():
    driver = initialize_driver()
    try:
        rows = fetch_data_from_url(driver)
        write_data_to_csv(rows)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
